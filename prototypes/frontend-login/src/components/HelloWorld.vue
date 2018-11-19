<template>
  <div class="hello">
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#">Thymesis</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor02" aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarColor02">
          <ul class="navbar-nav mr-auto">
          </ul>
          <form class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2" type="text" placeholder="e-mail">
            <input class="form-control mr-sm-2" type="text" placeholder="password">
            <button class="btn btn-info my-2 my-sm-0" type="submit">Login</button>
          </form>
        </div>
      </nav>
      <br>
      <div class="jumbotron">
        <h1>Thymesis</h1>
        <br>
        <div class="form-group">
          <input class="form-control form-control-lg" type="text" placeholder="Search memories..." id="inputLarge">
        </div>
        <img src="/img/tags.png" alt="" srcset="">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
