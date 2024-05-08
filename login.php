<?php
### ### ###  ### ### ###  ### ### ###
### ### ###   Universal   ### ### ###
### ### ###   includes    ### ### ###
session_start();
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';
include './assets/languages.php';

/*  
// ROUTES doesn't work
$routes = include "./assets/routes.php";

if (isset($routes[$language][$urlParameter])) {
    $targetPath = $routes[$language][$urlParameter];
} else {
    // default redirect if URL parameter not found
    $targetPath = $routes[$language]['index'];
}

// perform the redirect
header("Location: $targetPath", true, 301);
exit();
*/

$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
### ### ###  ### ### ###  ### ### ###
### ### ###  / Universal  ### ### ###
### ### ###  / includes   ### ### ###

session_start();
$loName = null;
$loPassword = null;
$chyba = null;



try {
    $pdo = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // Nastavení režimu chybových výjimek na výjimky
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
//    echo "Connection failed: " . $e->getMessage();
}

//catching login process
if (array_key_exists("login", $_POST)) {
    $loName = $_POST["meno"];
    $loPassword = $_POST["heslo"];
    
    //loading from the database by user name
    $sql = $pdo->prepare("SELECT * FROM users WHERE Username =? LIMIT 1");
    $sql->execute([$loName]);
    $result = $sql->fetch();
    
    if ($sql->rowCount() > 0) {
    
	//password protection
    $hashed_password = $result['PasswordHash'];
    
    //checking whether the entered password matches the password in the database
    if ($result && password_verify($loPassword, $hashed_password)){
        header("Location: ./index.php");
         $_SESSION["prihlasenyUzivatel"] = $loName;
       }
    
    //the user entered invalid data
    else 
    {
		$chyba = "Incorrect login information. Please try again.";
    }
    }

  }
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link rel="stylesheet" href="path/to/font-awesome/css/font-awesome.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="./css/login.css">

</head>
<body>
<main class="form-signin w-100 m-auto text-center mt-5">
  <form method="post">
    
    <h1 class="h3 mb-3 fw-normal" id="hacko">Sign in </h1>

    <div class="form-floating">
      <input type="text" class="form-control" id="floatingInput" placeholder="name@example.com" name="meno">
      <label for="floatingInput">Name</label>
    </div>
   
    <div class="form-floating">
      <input type="password" class="form-control" id="floatingPassword" placeholder="Password" name="heslo">
      <label for="floatingPassword">Password</label>
    </div> 

	<?php if ($chyba): ?>
                <p><?php echo $chyba; ?></p>
            <?php endif; ?>
	
	<button class="btn btn-primary w-100 py-2" type="submit" name="login">Sign in</button>
    <a href="./registration.php" id="acko">New user? Let´s create a account -></a>

	
    
    
                    
    
  </form>
</main>



</body>
