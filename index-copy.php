<?php
session_start();
// ### ### ###  ### ### ###  ### ### ###
// ### ### ###   INCLUDES   ### ### ###
// ### ### ###  ### ### ###  ### ### ###
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';

//$routes = include "./assets/routes.php";

include './assets/languages.php';
$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
// ### ### ###  ### ### ###  ### ### ###
// ### ### ###  / INCLUDES   ### ### ###
// ### ### ###  ### ### ###  ### ### ###


$welcome_message = '';
$welcome_message_new_user = '';
if (isset($_GET['success']) && $_GET['success'] == 'new') {
    $welcome_message_new_user = "<div class='alert alert-success' role='alert'>Vítejte na našem webu! Vaše registrace byla úspěšná.</div>";
}
if (isset($_GET['success']) && $_GET['success'] == 'logout') {
    $welcome_message_new_user = "<div class='alert alert-success' role='alert'>Odhlášení bylo úspěšné.</div>";
}

if (isset($_SESSION["username"])) {
    $username = $_SESSION["username"];
    $welcome_message = "Vítejte, <strong>$username</strong>! Jsme rádi, že jsi tu.";
} else {
    $welcome_message = "Vítejte na našem webu! Pro plný přístup prosím <a href='./prihlaseni.php'>přihlaste se</a> nebo <a href='./registrace'>vytvořte účet</a>.";
}

//navbar logout 
if(array_key_exists('logout', $_POST))
{
   unset($_SESSION['username']);
   header("Location: ?");
}



?>
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $translations['index_title'] ?></title>
    <!-- BOOTSTRAP -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">
	<link rel="stylesheet" href="css/index.css">
</head>
<body>

<?php include "includes/header.php"; ?>

<!-- NAVBAR -->
<div class="container-md">
<nav class="navbar bg-body-secondary fixed-top mb-4 ">
      <div class="container-xxl">
        <a class="navbar-brand" href="#">FDK</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
                <?php if(array_key_exists('username', $_SESSION)){
                echo "Prihlašený uživatel : $username";
            }
            else {
                echo '<a href="./prihlaseni.php">Prihlašte se</a>';
            }
            
            ?>
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                <a class="nav-link " aria-current="page" href="#">Můj účet</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Moje projekty</a>
              </li>
              <li class="nav-item">
              <a class="nav-link" href="#">Moje úkoly</a>
            </li>
             
               
            <form class="d-flex mt-3" role="search" method="post">
                <?php if(array_key_exists('username', $_SESSION)){
                    echo '<button class="btn btn-outline-danger" type="submit" name="logout">Logout</button>';
                }
                ?>
             
            </form>
          </div>
        </div>
      </div>
    </nav>
</div>
    <!-- END OF NAVBAR --> 


<div class="container mt-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-3 d-none d-md-block">
            <div class="sidebar-module">
                <!--<h3>Testovací provoz</h3>-->
                <!-- Obsah sidebaru -->
<?php
                if (isset($_SESSION["user_id"])) {
    $user_id = $_SESSION["user_id"];

    // SQL dotaz na výběr projektů
    $stmt = $pdo->prepare("SELECT * FROM FDK_projects WHERE owner_id = ? ORDER BY created DESC LIMIT 5");
    $stmt->execute([$user_id]);
    $projects = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Kontrola, jestli existují nějaké projekty
    if (count($projects) > 0) {
        echo "<h4>Moje projekty</h4>";
        echo "<ul>";
        foreach ($projects as $project) {
            echo "<li style='list-style-type:none;margin-left:-30px'><a href='/" . htmlspecialchars($project['url']) . "'>" . htmlspecialchars($project['name']) . "</a></li>";
        }
        echo "</ul>";
    } else {
        echo "<p>Žádné projekty nebyly nalezeny.</p>";
    }
    
echo "<p><small><a href='./odhlaseni'>Odhlásit</a></small></p>";

                
} else {

echo "<p>Pro zobrazení projektů se musíte <a href='/prihlaseni'>přihlásit</a>.</p>";

}
?>
            </div>
            <div class="sidebar-module">
                <?php echo $translations['index_sidebar_text'] ?>
            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">
            
                        <?= $welcome_message_new_user ?>

            <p><?php echo $welcome_message; ?></p>
            <!--Vítejte v novém a jedinečném nástroji pro správu úkolů, který přináší revoluční 
            možnosti spolupráce a efektivity. 
            Tento nástroj je něčím, o čem jste dosud jen snili, ale teď je to skutečností, 
            kterou můžete okamžitě využít zdarma.-->
            <p><?php echo $translations['index_text'] ?></p>

            </div>
        </div>
    </div>
</div>




    <!-- Main Content -->
    <div class="container mt-5">
        <div class="row">
            <!-- Obsah (zabere celou šířku na mobilu a tabletu, tedy i v řádku) -->
            <div class="col-12">
                <div class="task-board">
                    <!-- To-Do Column -->
                    <div class="task-column">
                        <h3><?php echo $translations['to_do'] ?><!--To-Do--></h3>
                        <div class="task-card">
                            <h4>Úkol 1</h4>
                            <p>Přidat úkoly do správce úkolů </p>
                        </div>
                        <!--<div class="task-card">
                            <h4>Úkol 2</h4>
                            <p>Aktualizovat obsah webové stránky</p>
                        </div>-->
                    </div>
                    <!-- In Progress Column -->
                    <div class="task-column">
                        <h3><?php echo $translations['in_progress'] ?><!--In Progress--></h3>
                        <div class="task-card">
                            <h4>Úkol 2</h4>
                            <p>Vytvořit <a href="novy-projekt">nový projekt</a> a přidat tým</p>
                        </div>
                    </div>
                    <!-- Done Column -->
                    <div class="task-column">
                        <h3><?php echo $translations['done'] ?><!--Done--></h3>
                        <div class="task-card">
                            <h4>Úkol  3</h4>
                            <p>Sehnat nástroj pro správu úkolů. Zdarma!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>



    <!-- Full Width Module -->
    <div class="container xl">
	<h1 class="text-center">Vaše úkoly</h1>
		<div class="ukoly">
       
	   <div class="ukol text-center">
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
	   	<p><b>Vylepšit frontend</b></p>
	    <p>Martin -> Tristan</p>
		<p> vysoká</p>
		<p>Probíha</p>
		</div>
		
		<div class="ukol text-center">
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
		<p><b>Vylepšit frontend</b></p>
		<p>Zadal Martin -> Tristan</p>
		<p>Priorita : vysoká</p>
		<p>Probíha</p>
		</div>
		
		<div class="ukol text-center">
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
		<p><b>Vylepšit frontend</b></p>
		<p>Zadal Martin -> Tristan</p>
		<p>Priorita : vysoká</p>
		<p>Probíha</p>
		</div>
		
		<div class="ukol text-center">
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
		<p><b>Vylepšit frontend</b></p>
		<p>Zadal Martin -> Tristan</p>
		<p>Priorita : vysoká</p>
		<p>Probíha</p>
		</div>
		
		<div class="ukol text-center">
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
		<p><b>Vylepšit frontend</b></p>
		<p>Zadal Martin -> Tristan</p>
		<p>Priorita : vysoká</p>
		<p>Probíha</p>
		</div>
		<div class="ukol text-center">
		
		<!-- kategoria --> <img src="https://img.freepik.com/free-vector/computer-programming-camp-abstract-concept-illustration_335657-3921.jpg?w=740&t=st=1715671724~exp=1715672324~hmac=641e20463145d796f8ba48cfc3aac38ffa0d71cd01d7c3e5630413d3e9248a38" width="auto" alt="">
		<p><b>Vylepšit frontend</b></p>
		<p>Zadal Martin -> Tristan</p>
		<p>Priorita : vysoká</p>
		<p>Probíha</p>
		</div>




	   </div>
    </div>




<?php include "./includes/footer.php" ?>

</body>
</html>