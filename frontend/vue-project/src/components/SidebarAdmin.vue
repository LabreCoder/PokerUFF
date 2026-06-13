<template>
  <aside class="sidebar-admin" aria-label="Ações do administrador">
    <div class="action-item">
      <button
        type="button"
        class="action-button"
        aria-label="Revelar votos"
        @click="emit('reveal-votes')"
      >
        <i class="mdi mdi-eye"></i>
      </button>

      <span class="action-label">Revelar votos</span>
    </div>

    <div class="action-item">
      <button
        type="button"
        class="action-button"
        aria-label="Reiniciar votação"
        @click="emit('reset-votes')"
      >
        <i class="mdi mdi-refresh"></i>
      </button>

      <span class="action-label">Reiniciar votação</span>
    </div>

    <div class="action-item">
      <button
        type="button"
        class="action-button"
        aria-label="Excluir sessão"
        @click="emit('delete-session')"
      >
        <i class="mdi mdi-delete"></i>
      </button>

      <span class="action-label">Excluir sessão</span>
    </div>
  </aside>
</template>

<script setup>
const emit = defineEmits([
  'reveal-votes',
  'reset-votes',
  'delete-session'
])
</script>

<style scoped>
.sidebar-admin {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 20;
  width: 168px;
  background: #1E1E1E;
  border-top-left-radius: 26px;
  border-bottom-left-radius: 26px;
  padding: 28px 20px 28px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.action-button {
  width: 66px;
  height: 66px;
  border: none;
  border-radius: 50%;
  background: #565656;
  color: #FFF;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s ease, filter 0.2s ease;
  flex-shrink: 0;
}

.action-button:hover {
  transform: scale(1.05);
}

.action-button i {
  font-size: 30px;
  color: #FFF;
}

.action-label {
  color: #FFF;
  font-size: 13px;
  line-height: 1.2;
  text-align: center;
  max-width: 110px;
}
</style>