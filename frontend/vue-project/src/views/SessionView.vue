<template>
  <SessionCodeModal
    :show="showCodeModal"
    :code="sessionCode"
    @close="showCodeModal = false"
  />

  <UserNameModal
    :show="showUserNameModal"
    @confirm="setUsername"
  />

  <div class="session">
    <header class="header">
      <Divider class="header-divider" />
      <div class="logo-area">
        <img
          src="@/assets/img/logo.svg"
          alt="PokerUFF"
          class="logo"
        />
        <span class="logo-text">
          | PokerUFF
        </span>
      </div>

      <div class="header-right">
        <div class="session-title">
          {{ sessionName }}
        </div>
        <div class="share-wrapper">
          <button
            class="share-btn"
            @click="copyCode"
          >
            <i class="mdi mdi-share-variant"></i>
          </button>
          <div
            v-if="copied"
            class="copy-tooltip"
          >
            Código da sessão copiado
          </div>
        </div>
      </div>
    </header>

    <div class="content">
      <div class="leave-wrapper">
        <button
          class="leave-btn"
          @click="leaveSession"
        >
          <i class="mdi mdi-exit-to-app"></i>
        </button>

        <span class="leave-label">
          Sair
        </span>
      </div>
      <h1 class="title">Clique em um cartão para votar</h1>
      <div class="cards">
        <div
          v-for="value in cards"
          :key="value"
          class="card"
          @click="vote(value)"
        >
          {{ value }}
        </div>
      </div>

      <div class="participants">
        <h2>Participantes</h2>
        <div
          v-for="p in state.participants"
          :key="p"
          class="participant"
        >
          <span>{{ p }}</span>
          <span class="vote">
            <template v-if="!state.revealed">
              {{ state.votes[p] ? '✔' : '?' }}
            </template>
            <template v-else>
              {{ state.votes[p] ?? '-' }}
            </template>
          </span>
        </div>
      </div>

      <SidebarAdmin
        v-if="isAdmin"
        @reveal-votes="revealVotes"
        @reset-votes="resetVotes"
        @delete-session="deleteSession"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Divider from '@/components/Divider.vue'
import SessionCodeModal from '@/components/SessionCodeModal.vue'
import UserNameModal from '@/components/UserNameModal.vue'
import SidebarAdmin from '@/components/SidebarAdmin.vue'

const route = useRoute()
const router = useRouter()
const SESSION_CODE = route.params.code

const username = ref('')
const ws = ref(null)

const state = ref({
  participants: [],
  votes: {},
  revealed: false,
  admin: null,
  name: ''
})

const sessionName = ref('Sessão')
const isAdmin = ref(false)

const cards = [1, 2, 3, 5, 8, 13]

const showCodeModal = ref(false)
const sessionCode = ref('')
const showUserNameModal = ref(false)
const copied = ref(false)

async function copyCode() {
  await navigator.clipboard.writeText(SESSION_CODE)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2000)
}

function connect() {
  ws.value = new WebSocket(`ws://127.0.0.1:8000/ws/${SESSION_CODE}`)

  ws.value.onopen = () => {
    ws.value.send(JSON.stringify({
      type: 'sync'
    }))
  }

  ws.value.onmessage = (event) => {
    const msg = JSON.parse(event.data)

    if (msg.type === 'state') {
      state.value = msg.data

      sessionName.value = msg.data.name
      isAdmin.value = username.value === msg.data.admin
    }
  }

  ws.value.onclose = () => {
    if (router.currentRoute.value.path !== '/') {
      router.push('/')
    }
  }
}

async function joinSession(name) {
  try {
    const res = await fetch('http://127.0.0.1:8000/session/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code: SESSION_CODE,
        name
      })
    })

    if (!res.ok) {
      alert('Não foi possível entrar na sessão')
      router.push('/')
      return
    }

    if (!ws.value) {
      connect()
    }

  } catch (err) {
    alert('Erro ao conectar à sessão')
    router.push('/')
  }
}

async function setUsername(name) {
  username.value = name

  showUserNameModal.value = false

  await joinSession(name)
}

function vote(value) {
  if (!ws.value) return

  ws.value.send(JSON.stringify({
    type: 'vote',
    user: username.value,
    value
  }))
}

async function leaveSession() {

  await fetch('http://127.0.0.1:8000/session/leave', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: SESSION_CODE,
      name: username.value
    })
  })

  if (ws.value) {
    ws.value.close()
    ws.value = null
  }

  router.push('/')
}

async function revealVotes() {
  if (!isAdmin.value) return

  const res = await fetch('http://127.0.0.1:8000/session/reveal', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: SESSION_CODE,
      name: username.value
    })
  })

  if (!res.ok) {
    alert('Não foi possível revelar os votos')
  }
}

async function resetVotes() {
  if (!isAdmin.value) return

  const res = await fetch('http://127.0.0.1:8000/session/reset', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: SESSION_CODE,
      name: username.value
    })
  })

  if (!res.ok) {
    alert('Não foi possível reiniciar a votação')
  }
}

async function deleteSession() {
  if (!isAdmin.value) return

  const confirmed = window.confirm(
    'Tem certeza que deseja excluir esta sessão?'
  )

  if (!confirmed) {
    return
  }

  const res = await fetch('http://127.0.0.1:8000/session/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: SESSION_CODE,
      name: username.value
    })
  })

  if (!res.ok) {
    alert('Não foi possível excluir a sessão')
    return
  }

  if (ws.value) {
    ws.value.close()
    ws.value = null
  }

  router.push('/')
}

onMounted(async () => {
  const showSessionCodeModal =
    localStorage.getItem('showCodeModal') === 'true'

  if (showSessionCodeModal) {
    sessionCode.value = localStorage.getItem('sessionCode')
    showCodeModal.value = true
    localStorage.removeItem('showCodeModal')
    localStorage.removeItem('sessionCode')
  }

  const res = await fetch(`http://127.0.0.1:8000/session/${SESSION_CODE}`)

  if (!res.ok) {
    return
  }

  const data = await res.json()
  sessionName.value = data.name
  const pendingAdminName = localStorage.getItem('pendingAdminName')

  if (pendingAdminName) {
    username.value = pendingAdminName
    isAdmin.value = true

    localStorage.removeItem('pendingAdminName')
    await joinSession(pendingAdminName)

  } else {
    showUserNameModal.value = true
  }
})

onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<style scoped>
.session {
  background: #121212;
  min-height: 100vh;
  color: white;
}

.header {
  position: relative;

  height: 82px;
  background: #1E1E1E;

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 0 30px;
}

.header-divider {
  position: absolute;
  top: 0;
  left: 0;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-size: 24px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 18px;
}

.session-title {
  background: #121212;
  padding: 10px 24px;
  border-radius: 26px;
}

.share-wrapper {
  position: relative;
}

.share-btn {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;

  display: flex;
  justify-content: center;
  align-items: center;
}

.share-btn i {
  font-size: 28px;
}

.copy-tooltip {
  position: absolute;
  top: 40px;
  right: 0;
  background: #565656;
  color: white;
  padding: 10px 18px;
  border-radius: 16px;
  white-space: nowrap;
  font-size: 14px;
}

.logo {
  font-weight: 600;
}

.session-title {
  background: #121212;
  padding: 8px 16px;
  border-radius: 20px;
}

.content {
  padding: 120px 40px;
  position: relative;
}

.title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 40px;
}

.cards {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 60px;
}

.card {
  width: 120px;
  height: 180px;
  background: #565656;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  cursor: pointer;
  transition: 0.2s;
}

.card:hover {
  transform: scale(1.05);
}

.participants {
  max-width: 600px;
  margin: 0 auto;
}

.participant {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #1E1E1E;
}

.leave-wrapper {
  position: absolute;
  top: 30px;
  left: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.leave-btn {
  width: 58px;
  height: 58px;
  border: none;
  border-radius: 50%;
  background: #565656;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.leave-btn i {
  color: white;
  font-size: 30px;
}

.leave-label {
  color: white;
  font-size: 14px;
}
</style>