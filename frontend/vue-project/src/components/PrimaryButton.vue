<template>
  <button class="primary-button">
    <slot />
  </button>
</template>

<style scoped>
.primary-button {
  width: 100%;
  height: 58px;

  border: none;
  border-radius: 26px;

  cursor: pointer;

  font-family: 'Poppins', sans-serif;
  font-size: 18px;
  font-weight: 600;

  color: #121212;

  background: linear-gradient(
    270deg,
    #2BBCAB 0%,
    #29C2FA 33%,
    #2248FB 66%,
    #0079FD 100%
  );

  transition: 0.2s ease;
}

.primary-button:hover {
  opacity: 0.92;
}
</style>