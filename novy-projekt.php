<?php


### ### ###  ### ### ###  ### ### ###
# TEMP FILE UNTIL ROUTING WILL WORK #
### ### ###  ### ### ###  ### ### ###



session_start();
### ### ###  ### ### ###  ### ### ###
### ### ###   INCLUDES   ### ### ###
### ### ###  ### ### ###  ### ### ###
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
### ### ###  / INCLUDES   ### ### ###
### ### ###  ### ### ###  ### ### ###


if (isset($_SESSION["username"])) {
    $username = $_SESSION["username"];
    $user_id = $_SESSION["user_id"];
    $welcome_message = "";
} else {
    $username = '';
    $user_id = 'NULL';
    $welcome_message = "";
}



$error_message = '';
$success_message = '';
$form_data = $_SESSION['form_data'] ?? ['project_name' => '', 'project_description' => '', 'url' => '', 'public' => false];



if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['project_name'] ?? '';
    $description = $_POST['project_description'] ?? '';
    $url = prettyURL($_POST['url']) ?? '';
    $public = isset($_POST['public']) ? 1 : 0;

    // Zkontrolujte, zda uživatel je přihlášen
    if (!isset($_SESSION["user_id"]) || empty($_SESSION["user_id"])) {
        $error_message = "Uživatel není přihlášen. Prosím, přihlašte se.";
    } else {
        $user_id = $_SESSION["user_id"];  // Nastavení uživatelského ID z session

        // Kontrola existence URL
        $stmt = $pdo->prepare("SELECT COUNT(*) FROM FDK_projects WHERE url = ?");
        $stmt->execute([$url]);
        if ($stmt->fetchColumn() > 0) {
            $error_message = "URL již existuje, zvolte prosím jinou.";
        } else {
            $stmt = $pdo->prepare("INSERT INTO FDK_projects (name, description, url, public, owner_id, created) VALUES (?, ?, ?, ?, ?, NOW())");
            if ($stmt->execute([$name, $description, $url, $public, $user_id])) {
                $project_id = $pdo->lastInsertId();  // Získání ID nově vytvořeného projektu
                $creator_ip = $_SERVER['REMOTE_ADDR'];  // Získání IP adresy uživatele
                
                // Vložení IP adresy do tabulky FDK_IP
                $stmt = $pdo->prepare("INSERT INTO FDK_ip (project_id, name, ip_range) VALUES (?, ?, ?)");
                $stmt->execute([$project_id, 'Creator', $creator_ip]);

                $success_message = "Projekt <a href='/$url'>$name</a> byl úspěšně vytvořen!<br> <a href='/$url'>Přejít na projekt $name</a>";
            } else {
                $error_message = "Chyba při vytváření projektu.";
            }
        }
    }
}


?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Task Management</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">

</head>
<body>



<?php include "includes/header.php"; ?>



<div class="container mt-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-3 d-none d-md-block">
            <div class="sidebar-module">
                <!--<h3>Testovací provoz</h3>-->
<?php
if (isset($_SESSION["username"])) {
    echo $username;
    echo "<br>";
} else {
}
?>
                <?php echo $translations['new_project_left_sidebar'] ?>

            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">


            <h2><?php echo $translations['new_project_form_title'] ?></h2>
        <?php if (!empty($success_message)) echo "<div class='alert alert-success'>$success_message</div>";  ?>
        <?php if (!empty($error_message)) echo "<div class='alert alert-danger'>$error_message</div>"; ?>

<form action="" method="post">
    <div class="mb-3">
        <label for="project_name" class="form-label"><?php echo $translations['new_project_form_name'] ?></label>
        <input type="text" class="form-control" id="project_name" name="project_name" value="<?php echo htmlspecialchars($form_data['project_name']); ?>" required>
    </div>
    <div class="mb-3">
        <label for="url" class="form-label"><?php echo $translations['new_project_form_url'] ?></label>
        <input type="text" class="form-control" id="url" name="url" value="<?php echo htmlspecialchars($form_data['url']); ?>" required>
    </div>
    <div class="mb-3">
        <label for="project_description" class="form-label"><?php echo $translations['new_project_form_description'] ?></label>
        <textarea class="form-control" id="project_description" name="project_description" rows="3" required><?php echo htmlspecialchars($form_data['project_description']); ?></textarea>
    </div>
    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" id="public" name="public" <?php echo $form_data['public'] ? 'checked' : ''; ?>>
        <label class="form-check-label" for="public" title="<?php echo $translations['new_project_form_checkbox_title'] ?>"><?php echo $translations['new_project_form_checkbox'] ?></label>
    </div>
    <input type="hidden" class="form-control" id="owner_id" name="owner_id" value="<?php echo $user_id; ?>">
    <button type="submit" class="btn btn-primary"><?php echo $translations['new_project_form_button'] ?></button>
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

<?php include "./includes/footer.php" ?>

</body>
</html>
