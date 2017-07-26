<template>
  <li class="list-group-item">
    {{ person.name }} {{ person.surname }}
    <button v-on:click="select(person)">Seleccionar</button>
  </li>
</template>
<script>
  export default {
    props: ['person'],
    methods: {
      select: function (person) {
        this.$emit('selected', person.id)
      }
    }
  }
</script>
