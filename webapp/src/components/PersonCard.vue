<template>
  <div class="person-card" @click="select">
    [[[[[[DNI]]]]]] - {{ person.name }} {{ person.surname }}
  </div>
</template>
<script>
  export default {
    props: ['person'],
    methods: {
      select: function () {
        this.$emit('selectPerson', this.person.id)
      }
    }
  }
</script>

<style scoped>
  .person-card {

  }
</style>
