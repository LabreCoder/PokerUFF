<template>
  <div class="container">

    <h1>Criar sessão</h1>

    <input v-model="sessionName" placeholder="Nome da sessão" />
    <input v-model="username" placeholder="Seu nome (admin)" />

    <div>
      <label>
        <input type="checkbox" v-model="settings.showAverage" />
        Exibir média
      </label>

      <label>
        <input type="checkbox" v-model="settings.showMedian" />
        Exibir mediana
      </label>

      <label>
        <input type="checkbox" v-model="settings.showParticipants" />
        Exibir nomes
      </label>
    </div>

    <!-- estimativas fixas por enquanto -->
    <div>
      <span v-for="card in cards" :key="card">
        {{ card }}
      </span>
    </div>

    <button @click="createSession">
      Criar
    </button>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const sessionName = ref('')
const username = ref('')

const settings = ref({
  showAverage: true,
  showMedian: false,
  showParticipants: true
})

const cards = [1, 2, 3, 5, 8, 13]

const createSession = async () => {
  if (!sessionName.value || !username.value) return

  const response = await fetch('http://127.0.0.1:8000/session/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: sessionName.value
    })
  })

  const data = await response.json()

  // redireciona para a sala
  router.push(`/session/${data.code}`)
}
</script>