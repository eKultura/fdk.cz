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


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['category_name'] ?? '';
    $description = $_POST['category_description'] ?? '';

    // SQL to insert data into FDK_Categories
    $sql = "INSERT INTO FDK_categories (name, description) VALUES (:name, :description)";
    $stmt = $conn->prepare($sql);
    if ($stmt) {
        $stmt->bindParam(":name", $name);
        $stmt->bindParam(":description", $description);
        $stmt->execute();
        if ($stmt->rowCount() > 0) {
            $success_message = "Success";
        } else {
            $error_message = "Error: " . $stmt->errorInfo()[2];
        }
        $stmt->closeCursor();
    } else {
        $error_message = "Error: " . $conn->errorInfo()[2];
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vytvořit novou kategorii</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Create new category</h1>
        <?php if (!empty($success_message)) echo "<div class='alert alert-success'>$success_message</div>"; ?>
        <?php if (!empty($error_message)) echo "<div class='alert alert-danger'>$error_message</div>"; ?>
        <form action="" method="post">
            <div class="mb-3">
                <label for="category_name" class="form-label">Name</label>
                <input type="text" class="form-control" id="category_name" name="category_name" required>
            </div>
            <div class="mb-3">
                <label for="category_description" class="form-label">Description</label>
                <textarea class="form-control" id="category_description" name="category_description" rows="3" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Create category</button>
        </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
