<template>
  <main class="app-shell">
    <header class="topbar">
      <RouterLink class="brand" to="/">智学工坊</RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">画像</RouterLink>
        <RouterLink to="/generate">生成</RouterLink>
        <RouterLink to="/resources">资源</RouterLink>
        <RouterLink to="/path">路径</RouterLink>
        <RouterLink to="/quiz">测验</RouterLink>
      </nav>
    </header>

    <RouterView />
  </main>
</template>
