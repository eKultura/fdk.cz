<?php
include "./includes/db_connection.php"; 
include "./includes/settings.php"; 

$translations = include "./assets/translations/$language.php";

$urlParameter = isset($_GET['url']) ? $_GET['url'] : 'home'; // Default value if no URL parameter is provided

// Define routes
$routes = include "./assets/routes.php";

// Check if the route exists for the current language
if (isset($routes[$language][$urlParameter])) {
    // If the route exists, include the corresponding file
    include "./" . $routes[$language][$urlParameter];
} else {
    // If the route doesn't exist, include a 404 error page or redirect to the homepage
    include "./404.php"; // Assuming you have a 404.php file for handling not found pages
}


?><!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>404</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">
</head>
<body>

<?php include "includes/header.php"; ?>


<div class="container mt-5">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">
            <!--Vítejte v novém a jedinečném nástroji pro správu úkolů, který přináší revoluční 
            možnosti spolupráce a efektivity. 
            Tento nástroj je něčím, o čem jste dosud jen snili, ale teď je to skutečností, 
            kterou můžete okamžitě využít zdarma.-->
            <h1>404</h1>

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
                            <p>Vytvořit nový projekt a přidat tým</p>
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
                            <!-- Pět vzorových úkolů -->
                            <tr>
                                <td>Sehnat nástroj pro správu úkolů</td>
                                <td>Vysoká</td>
                                <td class="mobile">Dokončeno</td>
                                <td>Martin</td>
                                <td>Projekt</td>
                                <td class="tablet mobile">Barča</td>
                            </tr>
                            <!-- Další vzorové úkoly -->
                            <!-- ... -->

                            <!-- Dva náhodně přidělené podúkoly -->
                            <tr>
                                <td class="small">Vytvořit strukturu</td>
                                <td class="small">Střední</td>
                                <td class="small mobile">Probíhá</td>
                                <td class="small">Tristan</td>
                                <td class="small">Frontend</td>
                                <td class="small tablet mobile">Barča</td>
                            </tr>
                            <tr>
                                <td>Aplikace na iPhone</td>
                                <td>Střední</td>
                                <td class="mobile">Probíhá</td>
                                <td class="">Bershee</td>
                                <td class="">iOS</td>
                                <td class="tablet mobile">Bershee</td>
                            </tr>
                            <!-- ... -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>




<?php include "./includes/footer.php" ?>

</body>
</html>
