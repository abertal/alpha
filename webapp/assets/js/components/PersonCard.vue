<template>
  <li class="list-group-item">
    <span v-bind:class="{ 'text-primary': selectedId == person.id }">
      {{ person.name }} {{ person.surname }}
    </span>
    <button v-on:click="select(person)">Seleccionar</button>
  </li>
</template>
<script>
  export default {
    props: ['person', 'selectedId'],
    methods: {
      select: function (person) {
        this.$emit('selected', person.id)
      }
    }
  }
</script>
