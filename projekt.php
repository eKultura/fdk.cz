<?php
session_start();
### ### ###  ### ### ###  ### ### ###
### ### ###   INCLUDES   ### ### ###
### ### ###  ### ### ###  ### ### ###
include './includes/db_connection.php';
include './includes/settings.php';
include './includes/functions.php';

//$routes = include "./assets/routes.php";

include './assets/languages.php';
$translations = include "./assets/translations/$language.php";

if (isset($_GET['lang']) && array_search($_GET['lang'], $languages) !== false) {
    $language = $_GET['lang'];
}
### ### ###  ### ### ###  ### ### ###
### ### ###  / INCLUDES   ### ### ###
### ### ###  ### ### ###  ### ### ###


### ### ###  DEBUG MODE  ### ### ### 
#ini_set('display_errors', 1);
#ini_set('display_startup_errors', 1);
#error_reporting(E_ALL);
### ### ### /DEBUG MODE  ### ### ###



$projectURL = $_GET['url'] ?? '';
$question = $pdo->prepare("SELECT project_id, name, description, url, public, created FROM FDK_projects WHERE url = ?");
$question->execute([$projectURL]);
$answer = $question->fetch();

if (!$answer) {
    die("Projekt nenalezen.");
}

if (isset($_SESSION["username"])) {
        $_SESSION['project_id'] = $answer['project_id'];
} else {
}

### SELECT * FROM FDK_tasks WHERE ParentID = [ParentID];
### SELECT * FROM FDK_tasks WHERE task_id = (SELECT ParentID FROM FDK_tasks WHERE task_id = [ID Child]);


$tasks = fetchTasksForProject($answer['project_id']);

function fetchTasksForProject($project_id) {
    global $pdo;
    $sql = "SELECT task_id, title, priority_id, status, created, due_date FROM FDK_tasks WHERE project_id = ? AND status IN ('Hotovo', 'Ke zpracování', 'Probíhá') ORDER BY status, created DESC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([$project_id]);
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
    // Výpis pro kontrolu
    //echo "<pre>"; print_r($result); echo "</pre>";
    return $result;
}






?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?php echo $answer['url'] ?>: Správce úkolů</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">

</head>
<body>
    <!-- Header -->
    <header class="bg-light py-4">
        <div class="container text-center">
            <h1 class="mb-0">Správce úkolů <?php echo $answer['name']; ?></h1>
        </div>
    </header>


<div class="container mt-5">
    <div class="row">
        <div class="col-md-12">
            <div class="sidebar-module">

                <p><?php echo $answer['description'] ?></p>

            </div>
        </div>
    </div>

    
<button onclick="toggleContent()" class="btn btn-primary" id="toggleButton">Skrýt stav úkolů</button>
<a href="/novy-ukol?projekt=<?php echo $answer['url'];?>" class="btn btn-primary">Nový úkol</a>

    <!-- JavaScript pro skrytí/zobrazení obsahu -->
    <script>
        // Funkce pro skrytí/zobrazení obsahu
        function toggleContent() {
            var content = document.getElementById('3col');
            var button = document.getElementById('toggleButton');
            if (content.style.display === 'none') {
                content.style.display = 'block';
                button.innerHTML = 'Skrýt stav úkolů';
            } else {
                content.style.display = 'none';
                button.innerHTML = 'Zobrazit stav úkolů';
            }
        }

        // Skrýt obsah při načtení stránky
        document.addEventListener('DOMContentLoaded', function() {
            var content = document.getElementById('3col');
            content.style.display = 'block';
        });
    </script>

<div class="container mt-5" id="3col">
    <div class="row">
        <div class="col-12">
            <div class="task-board">
                <?php
                // Rozdělení úkolů podle stavu
                $tasksBystatus = ['Ke zpracování' => [], 'Probíhá' => [], 'Hotovo' => []];
                foreach ($tasks as $task) {
                    $tasksBystatus[$task['status']][] = $task;
                }

                foreach ($tasksBystatus as $status => $tasksInstatus) {
                    echo "<div class='task-column'>";
                    echo "<h3>" . htmlspecialchars($status) . "</h3>";
                    $count = 0;
                    foreach ($tasksInstatus as $task) {
                        if ($count >= 5) break;  // Omezení na zobrazení max 5 úkolů pro každý stav
                        echo "<div class='task-card'>";
                        echo "<h4>Úkol " . htmlspecialchars($task['task_id']) . "</h4>";
                        echo "<p><a href='/detail-ukolu?id=" . $task["task_id"] . "'>" . htmlspecialchars($task['title']) . "</a></p>";
                        echo "</div>";
                        $count++;
                    }
                    echo "</div>"; // Konec sloupce pro daný stav
                }
                ?>
            </div>
        </div>
    </div>
</div>






<!-- Full Width Module -->
<div class="container mt-5">
    <div class="row">
        <div class="col">
            <div class="full-width-module">
                <h3>Zobrazení úkolů</h3>
                <table class="table">
                    <thead class="table-dark">
                        <tr>
                            <th><span class="mobile">Název úkolu</span><span class="pc">Úkol</span></th>
                            <th><span class="mobile">Priorita</span><span class="pc">Prio.</span></th>
                            <th class="mobile">Stav</th>
                            <th><span class="mobile">Přiděleno</span><span class="pc">Přid.</span></th>
                            <th><span class="mobile">Kategorie</span><span class="pc">Kat.</span></th>
                            <th class="tablet mobile">Zadal</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        // Dotaz do databáze pro úkoly
                                $projectID = $answer['project_id'];
                                

                                $sql = "SELECT * FROM FDK_tasks WHERE (status = 'Probíhá' OR status = 'Ke zpracování') AND project_id = :projectID ORDER BY task_id DESC LIMIT 100";
                                $stmt = $pdo->prepare($sql);
                                $stmt->execute(['projectID' => $projectID]);

                        if ($stmt->rowCount() > 0) {
                            // Výstup dat každého úkolu
                            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                                echo "<tr>";
                                echo "<td><a href='/detail-ukolu?id=" . $row["task_id"] . "'>" . $row["title"] . "</a></td>";
                                echo "<td class='" . $row["priority"] . "'>" . $row["priority"] . "</td>";
                                echo "<td class='mobile'>" . $row["status"] . "</td>";
                                echo "<td>" . $row["assigned"] . "</td>";
                                echo "<td>" . $row["category"] . "</td>";
                                echo "<td class='tablet mobile'>" . $row["creator"] . "</td>";
                                echo "</tr>";
                            }
                        } else {
                            echo "<tr><td colspan='6'>Žádné úkoly k zobrazení.</td></tr>";
                        }
                        ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>



<?php include "./includes/footer.php" ?>



</body>
</html>
