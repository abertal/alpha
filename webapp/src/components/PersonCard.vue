<template>
  <div class="person-card" @click="select">
    <span class="btn btn-primary btn-add">
      <div class="icon dripicons-plus"></div>
    </span>
      {{ person.name }} {{ person.surname }} {{ person.birthday }}
  </div>
</template>
<script>
  export default {
    props: ['person'],
    methods: {
      select: function () {
        this.$emit('selectPerson', this.person)
      }
    }
  }
</script>

<style scoped lang="less">
  .person-card {
    cursor: pointer;
    .btn-add {
      margin-right: 10px;
    }
  }
</style>
