<template>
  <div class="page">
    <header class="header">
      <Divider class="header-divider" />
      <div class="logo-area">
        <img
          src="@/assets/img/logo.svg"
          alt="PokerUFF"
          class="logo"
        />
        <span class="logo-text">| PokerUFF</span>
      </div>
    </header>

    <main class="main-content">
      <section class="left-grid">
        <img
          src="@/assets/img/pokeruff-slogan.svg"
          alt="PokerUFF"
          class="slogan"
        />
        <img
          src="@/assets/img/kanban-illustration.svg"
          alt="Kanban"
          class="illustration"
        />
      </section>
      <section class="right-grid">
        <div class="card">
          <div class="section">
            <h2>Entrar em uma sessão</h2>
            <div class="join-input-wrapper">
              <input
                v-model="joinCode"
                placeholder="Código da sessão"
                class="input"
              />
              <button
                class="join-button"
                @click="joinSession"
              >
                <img
                  src="@/assets/img/leave-icon.svg"
                  alt="Entrar"
                />
              </button>
            </div>
          </div>

          <div class="divider-spacing">
            <Divider />
          </div>

          <div class="section">
            <h2>Criar nova sessão</h2>
            <input
              v-model="createName"
              placeholder="Seu nome"
              class="input"
            />
            <input
              v-model="sessionName"
              placeholder="Nome da sessão"
              class="input"
            />
            <PrimaryButton class="primary-button" @click="createSession">
              Criar
            </PrimaryButton>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Divider from '@/components/divider.vue'
import PrimaryButton from '@/components/PrimaryButton.vue'

const router = useRouter()
const joinName = ref('')
const joinCode = ref('')
const createName = ref('')
const sessionName = ref('')

// JOIN SESSION
const joinSession = async () => {

  if (!joinCode.value) {
    alert('Digite o código da sessão')
    return
  }

  const username = prompt('Digite seu nome')

  if (!username) return

  joinName.value = username

  try {

    const code = joinCode.value.toUpperCase()

    const res = await fetch('http://127.0.0.1:8000/session/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code,
        name: joinName.value
      })
    })

    const data = await res.json()

    if (!res.ok || data.error) {
      alert(data.error || 'Erro ao entrar na sessão')
      return
    }

    localStorage.setItem('username', joinName.value)

    router.push(`/session/${code}`)

  } catch (err) {
    alert('Erro ao conectar com o servidor')
  }
}

// CREATE SESSION
const createSession = async () => {

  if (!createName.value || !sessionName.value) {
    alert('Preencha todos os campos')
    return
  }

  try {

    const res = await fetch('http://127.0.0.1:8000/session/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: sessionName.value
      })
    })

    const data = await res.json()

    if (!data.code) {
      alert('Erro ao criar sessão')
      return
    }

    const code = data.code

    await fetch('http://127.0.0.1:8000/session/join', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        code,
        name: createName.value
      })
    })

    localStorage.setItem('username', createName.value)
    router.push(`/session/${code}`)

  } catch (err) {
    alert('Erro ao criar sessão')
  }
}
</script>

<style scoped>

* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #121212;
  color: white;
  overflow-x: hidden;
}

.header {
  position: relative;
  height: 82px;
  width: 100%;
  background: #1E1E1E;
  display: flex;
  align-items: center;
  padding-left: 20px;
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
  margin-left: 12px;
}

.logo-text {
  font-size: 24px;
  font-weight: 600;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1.1fr;
  min-height: calc(100vh - 82px);
  width: 100%;
  padding: 20px 0;
}

.left-grid {
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
}

.slogan {
  width: clamp(180px, 28vw, 500px);
  height: auto;
  align-self: center;
}

.illustration {
  width: clamp(300px, 42vw, 900px);
  height: auto;
  align-self: flex-start;
  margin-left: 0;
}

.right-grid {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  width: clamp(320px, 40vw, 620px);
  background: #1E1E1E;
  border-radius: 16px;
  padding:
    clamp(24px, 5vh, 72px)
    clamp(20px, 2vw, 48px);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.divider-spacing {
  width: 100%;
  margin: 40px 0;
}

.section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(12px, 1.5vh, 20px);
}

.section h2 {
  font-size: clamp(20px, 1.5vw, 28px);
  font-weight: 600;
  text-align: center;
}

.input {
  width: 100%;
  height: clamp(50px, 5vh, 62px);
  background: #121212;
  border: none;
  outline: none;
  border-radius: 26px;
  padding: 0px 20px;
  color: white;
  font-size: clamp(14px, 1vw, 16px);
  margin: 2px;
}

.join-input-wrapper {
  position: relative;
  width: 100%;
  max-width: 520px;
}

.join-button {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;
  background: #1E1E1E;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.join-button img {
  width: 20px;
  height: 20px;
}

.primary-button {
  margin-top: 8px;
  width: 180px;
  height: 54px;
  border: none;
  border-radius: 26px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  color: #121212;
  background: linear-gradient(
    270deg,
    #2BBCAB,
    #29C2FA,
    #2248FB,
    #0079FD
  );
  transition: 0.2s;
}
</style>