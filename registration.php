<?php

$name = null;
$password = null;
$email = null;
$date = date("d. m. Y");


//DATABASE CONNECTION 
$servername = "46.28.109.13";
$username = "div_tristan";
$password = "div_@85ax987+258xi_fdk";
$dbname = "fdkDB";


try {
    $pdo = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // Nastavení režimu chybových výjimek na výjimky
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
//    echo "Connection failed: " . $e->getMessage();
}

//CREATING ACC AFTER CLICK ON REGISTER BUTTON
if (array_key_exists("register", $_POST)) {
    $name = $_POST["name"];
    $password = $_POST["password"];
    $email = $_POST["email"];
    

// HASING PASSWORD
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);
    
//INSERTING INTO DATABASE VALUES FROM INPUTS
    $sql = $db->prepare("INSERT INTO `users`(`Username`, `PasswordHash`, `Email`, `Created` ) VALUES ('$name','$hashed_password', '$email', '$date')");
    $sql->execute();
    header("Location: ./login.php");
    }
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="./css/registration.css">
</head>

<body>
<main class="form-signin w-100 m-auto text-center mt-5">
  <form method="post">
    
    <h1 class="h3 mb-3 fw-normal">Sign up</h1>

    <div class="form-floating">
      <input type="email" class="form-control mb-2" id="floatingInput" placeholder="email" name="email">
      <label for="floatingInput">Email</label>
    </div>

    <div class="form-floating">
      <input type="text" class="form-control mb-2" id="floatingInput" placeholder="login" name="name">
      <label for="floatingInput">Name</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control mb-2" id="floatingPassword" placeholder="Password" name="password">
      <label for="floatingPassword">Password</label>
    </div>

    <button class="btn btn-primary w-100 py-2" type="submit" name="register">Create account</button>
    <a href="./login.php" id="acko">Already have account? Let´s sign in -></a>
  
  </form>
</main>
</body>

</html>