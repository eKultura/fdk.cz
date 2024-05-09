<?php


### ### ###  ### ### ###  ### ### ###
# TEMP FILE UNTIL ROUTING WILL WORK #
### ### ###  ### ### ###  ### ### ###



session_start();
### ### ###  ### ### ###  ### ### ###
### ### ###   Universal   ### ### ###
### ### ###   includes    ### ### ###

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


$task_id = isset($_GET['id']) ? $_GET['id'] : die('Task ID is required.');

// Prepare and execute SQL query to fetch task details along with parent task and subtasks
$query = "
    SELECT t.*, c.name as category_name, p.name as priority_name, u.username as creator_name, 
           usr.username as assigned_to, prt.title as parent_title, prt.task_id as parent_id
    FROM FDK_tasks t
    LEFT JOIN FDK_categories c ON t.category_id = c.category_id
    LEFT JOIN FDK_priorities p ON t.priority_id = p.priority_id
    LEFT JOIN FDK_users u ON t.creator = u.user_id
    LEFT JOIN FDK_users usr ON t.assigned = usr.user_id
    LEFT JOIN FDK_tasks prt ON t.parent_id = prt.task_id
    WHERE t.task_id = :task_id
";
$stmt = $pdo->prepare($query);
$stmt->bindValue(':task_id', $task_id, PDO::PARAM_INT);
$stmt->execute();
$task = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$task) {
    echo "No task found with ID: $task_id";
    $pdo->close();
    exit;
}

// Query to fetch subtasks
$subtasks = [];
$subtask_query = "SELECT * FROM FDK_tasks WHERE parent_id = :parent_id";
$subtask_stmt = $pdo->prepare($subtask_query);
$subtask_stmt->bindValue(':parent_id', $task_id, PDO::PARAM_INT);
$subtask_stmt->execute();
$subtasks = $subtask_stmt->fetchAll(PDO::FETCH_ASSOC);
$subtask_stmt->closeCursor();

// No need to explicitly close statement or connection; they are closed automatically when script ends
?><!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detail úkolu</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <h1>Detail úkolu: <?= htmlspecialchars($task['title']); ?></h1>

    <div class="card">
        <div class="card-body">
            <h5 class="card-title"><?= htmlspecialchars($task['title']); ?></h5>
            <p><strong>Kategorie:</strong> <?= htmlspecialchars($task['category_name']); ?></p>
            <p><strong>Priorita:</strong> <?= htmlspecialchars($task['priority_name']); ?></p>
            <p><strong>Stav:</strong> <?= htmlspecialchars($task['status']); ?></p>
            <p><strong>Vytvořil:</strong> <?= htmlspecialchars($task['creator_name']); ?></p>
            <p><strong>Přiřazeno:</strong> <?= htmlspecialchars($task['assigned_to']); ?></p>
            <p><strong>Popis:</strong> <?= nl2br(linkify(htmlspecialchars($task['description']))); ?></p>
            <p><strong>Rodičovský úkol:</strong> <?= $task['parent_id'] ? '<a href="/ukol/detail.php?id=' . $task['parent_id'] . '">' . htmlspecialchars($task['parent_title']) . '</a>' : 'Žádný'; ?></p>

            <?php if (!empty($subtasks)): ?>
                <h4>Podúkoly:</h4>
                <ul>
                    <?php foreach ($subtasks as $subtask): ?>
                        <li><a href="/ukol/detail.php?id=<?= $subtask['task_id']; ?>"><?= htmlspecialchars($subtask['title']); ?></a></li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>
            <?php if (empty($task['parent_id'])): ?>
                <a href="/ukol/pridat.php?parent_id=<?= $task['task_id']; ?>&category=<?= $task['category_name']; ?>" class="btn btn-primary">Přidat nový podúkol</a>
            <?php endif; ?>
        </div>
    </div>

    <div class="card mt-3">
        <div class="card-body">
            <a href="/detail-ukolu?id=<?= $task_id; ?>" class="btn btn-secondary">Zpět na úkol</a>
            <a href="/upravit-ukol?id=<?= $task_id; ?>" class="btn btn-success">Editovat úkol</a>
            <a href="/pridat-komentar.php?id=<?= $task_id; ?>" class="btn btn-primary">Přidat komentář</a>
            <!-- Google Calendar Link -->
            <?php
            $startDate = date('Ymd\THis\Z', strtotime($task['created'])); // Start date as the creation date of the task
            $endDate = $task['due_date'] ? date('Ymd\THis\Z', strtotime($task['due_date'])) : date('Ymd\THis\Z', strtotime($task['created'] . ' +1 hour')); // End date as due date
            $googleLink = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" . urlencode($task['title']) . "&dates=" . $startDate . "/" . $endDate . "&details=" . urlencode("Assigned to: " . $task['assigned_to'] . "\nDescription: " . $task['description']) . "&location=" . urlencode($task['location'] ?? 'N/A');
            ?>
            <a href="<?= $googleLink ?>" target="_blank" class="btn btn-info">Přidat do Google kalendáře</a>
        </div>
    </div>
</div>
</body>
</html>


