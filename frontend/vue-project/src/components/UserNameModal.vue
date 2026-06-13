<template>
  <div
    v-if="show"
    class="overlay"
  >
    <div class="modal">
      <div class="text-container">
        <h1>
          Para entrar, informe seu nome
        </h1>
      </div>

      <input
        v-model="name"
        class="input"
        placeholder="Nome"
        @keyup.enter="confirm"
      >
      <div class="start-button">
        <PrimaryButton @click="confirm">
          Iniciar
        </PrimaryButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PrimaryButton from '@/components/PrimaryButton.vue'

const emit = defineEmits(['confirm'])

defineProps({
  show: {
    type: Boolean,
    required: true
  }
})

const name = ref('')

function confirm() {

  if (!name.value.trim()) {
    return
  }

  emit('confirm', name.value.trim())
}
</script>

<style scoped>

.overlay{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal{
  width: 500px;
  background:#1E1E1E;
  border-radius: 26px;
  padding: 40px 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.text-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

h1{
  margin: 10px 0px;
  color: white;
  font-size: 28px;
  font-weight: 600;
  text-align: center;
}

.input{
  width: 320px;
  height: 60px;
  background: #121212;
  border: none;
  outline: none;
  border-radius: 26px;
  padding: 0 20px;
  color: white;
  font-size: 16px;
}

.start-button{
  width: 180px;
  margin-top: 12px;
}

</style>