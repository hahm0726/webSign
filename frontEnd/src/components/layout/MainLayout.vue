<template>
  <v-app id="app">
    <header id="app-header">
      <span>인수증</span>
    </header>
    <v-main>
      <v-container id="contents-wrap" class="pt-2">
        <component :is="selectedComponent"></component>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Board from "/src/components/boards/Board";

export default {
  components: {
    Board,
  },
  computed: {
    //선택된 컴포넌트 반환
    selectedComponent: function () {
      return Board;
    },
  },
};
</script>

<style scoped>
#app-header {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 10vh;
  border: 2px solid;
}
#app {
  padding: 0;
  width: 100%;
}
#contents-wrap {
  min-height: 90vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>