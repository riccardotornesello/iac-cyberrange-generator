<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $db_host = getenv("DB_HOST") ?: "127.0.0.1";
  $db = new mysqli($db_host, 'challengeuser', '3b8743o4bf', 'admin_console');

  $username = $_POST['username'];
  $password = $_POST['password'];
  $sql = "SELECT * FROM users WHERE username = '{$username}' AND password = '{$password}'";

  $result = $db->query($sql);
  $count = $result->num_rows;

  if ($count == 1) {
    $flag = 'You did it. slntCTF{n0t_an0th3r_tIme}';
    $error = '';
  } else {
    $error = 'Invalid credentials';
    $flag = '';
  }
}
?>

<!DOCTYPE html>
<html>

<head>
  <title>Admin Console v2</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
  <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
</head>

<body>
  <div class="container">
    <h1>Admin console v2</h1>
    <p>Last year it was too easy to break into my console, so I improved it by inserting a database</p>
    <div class="row">
      <div style="margin:auto;position:absolute;top:0;left:0;bottom:0;right:0;width:50%;height:50%;">
        <form method="post">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" name="username" aria-describedby="emailHelp" placeholder="Enter username">
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="Password">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button><br>
          <?php
          if (!empty($error)) {
            echo "<div class='alert alert-danger' role='alert'>$error</div>";
          }
          if (!empty($flag)) {
            echo "<div class='alert alert-primary' role='alert'>$flag</div>";
          }
          ?>
        </form>
      </div>
    </div>
  </div>
</body>

</html>