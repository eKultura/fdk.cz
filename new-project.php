<?php
### ### ###  ### ### ###  ### ### ###
### ### ###   Universal   ### ### ###
### ### ###   includes    ### ### ###
session_start();
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';
include './assets/languages.php';

//$routes = include "./assets/routes.php";

$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
### ### ###  ### ### ###  ### ### ###
### ### ###  / Universal  ### ### ###
### ### ###  / includes   ### ### ###


// Fetch the route from the URL parameter
$urlParameter = $_GET['url'] ?? 'index';  // Default to 'index' if no parameter is provided

$routes = include "./assets/routes.php";

// Check if the requested URL parameter matches any defined route and handle it
if (!empty($routes[$language][$urlParameter])) {
    include $routes[$language][$urlParameter];
} else {
    echo "404 Not Found. The page you are looking for does not exist.";
}


/* === DEBUG ===

ob_start(); // Turn on output buffering
echo "URL Parameter Received: '$urlParameter'<br>";
echo "<pre>Routes Configuration: "; print_r($routes[$language]); echo "</pre>";

echo "Target path: $targetPath<br>";
exit(); // Remove after testing



header("Location: $targetPath", true, 301);
exit();
*/



if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['project_name'] ?? '';
    $description = $_POST['project_description'] ?? '';
    $url = $_POST['url'] ?? '';
    $public = isset($_POST['public']) ? 1 : 0;  // Checkbox for public

    // SQL to insert data into FDK_Projects
    $sql = "INSERT INTO FDK_projects (name, description, url, public, created) VALUES (:name, :description, :url, :public, NOW())";
    $stmt = $conn->prepare($sql);
    if ($stmt) {
        $stmt->bindParam(":name", $name);
        $stmt->bindParam(":description", $description);
        $stmt->bindParam(":url", $url);
        $stmt->bindParam(":public", $public, PDO::PARAM_INT);
        $stmt->execute();
        if ($stmt->rowCount() > 0) {
            $success_message = "Projekt byl úspěšně vytvořen!";
        } else {
            $error_message = "Chyba při vytváření projektu: " . $stmt->errorInfo()[2];
        }
        $stmt->closeCursor();
    } else {
        $error_message = "Chyba při přípravě dotazu: " . $conn->errorInfo()[2];
    }
}

?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Task Management</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/inc/project.css" crossorigin="anonymous">

</head>
<body>
    <!-- Header -->
    <header class="bg-light py-4">
        <div class="container text-center">
            <h1 class="mb-0">Správce úkolů</h1>
        </div>
    </header>


<div class="container mt-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-3 d-none d-md-block">
            <div class="sidebar-module">
                <!--<h3>Testovací provoz</h3>-->
                <!-- Obsah sidebaru -->
                Každý projekt má mít svoji doménu. 
                Pokud si doménu ověříte, projekt bude žít navěky. Pro neověřené domeny má projekt platnost 1 měsíc.
            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">


            <h2>Vytvořit Nový Projekt</h2>
        <?php if (!empty($success_message)) echo "<div class='alert alert-success'>$success_message</div>"; ?>
        <?php if (!empty($error_message)) echo "<div class='alert alert-danger'>$error_message</div>"; ?>

        <form action="" method="post">
            <div class="mb-3">
                <label for="project_name" class="form-label">Název Projektu</label>
                <input type="text" class="form-control" id="project_name" name="project_name" required>
            </div>
            <div class="mb-3">
                <label for="project_name" class="form-label">URL (věříme, že každý projekt má mít svoji doménu)</label>
                <input type="text" class="form-control" id="url" name="url" required>
            </div>
            <div class="mb-3">
                <label for="project_description" class="form-label">Popis Projektu</label>
                <textarea class="form-control" id="project_description" name="project_description" rows="3" required></textarea>
            </div>
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="public" name="public">
                <label class="form-check-label" for="public">Veřejný projekt</label>
            </div>
            <button type="submit" class="btn btn-primary">Vytvořit Projekt</button>
        </form>
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
                        <h3>K provedení<!--To-Do--></h3>
                        <div class="task-card">
                            <h4>Úkol 1</h4>
                            <p>Vytvořit první úkoly pro tým</p>
                        </div>
                    </div>
                    <!-- In Progress Column -->
                    <div class="task-column">
                        <h3>V procesu<!--In Progress--></h3>
                        <div class="task-card">
                            <h4>Úkol 2</h4>
                            <p>Zaregistrovat nový projekt na fdk.cz</p>
                        </div>
                    </div>
                    <!-- Done Column -->
                    <div class="task-column">
                        <h3>Hotovo<!--Done--></h3>
                        <div class="task-card">
                            <h4>Úkol  3</h4>
                            <p>Sehnat nástroj pro správu úkolů. Zdarma!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

<?php include "./inc/footer.php" ?>

</body>
</html>
