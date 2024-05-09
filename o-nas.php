<?php


### ### ###  ### ### ###  ### ### ###
# TEMP FILE UNTIL ROUTING WILL WORK #
### ### ###  ### ### ###  ### ### ###




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


?>
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>O nás</title>

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
                <!-- Obsah sidebaru -->
                <?php echo $translations['index_sidebar_text'] ?>
            </div>
        </div>
        <!-- Obsah -->
        <div class="col-md-9 col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">
            <!--Vítejte v novém a jedinečném nástroji pro správu úkolů, který přináší revoluční 
            možnosti spolupráce a efektivity. 
            Tento nástroj je něčím, o čem jste dosud jen snili, ale teď je to skutečností, 
            kterou můžete okamžitě využít zdarma.-->
            <p>Vítejte u nás! Jsme tým nadšenců, kteří se spojili, aby vytvořili nástroj pro správu úkolů, 
            který by splnil všechny naše potřeby – a teď je k dispozici i pro vás, zcela zdarma.</p>

<p>Naše cesta začala, když jsme hledali ideální řešení pro správu našich projektů, ale 
žádný z dostupných nástrojů nám nevyhovoval úplně. Rozhodli jsme se vzít věci do vlastních rukou. 
Výsledkem je platforma, která je intuitivní, flexibilní a plně přizpůsobitelná různým týmovým a 
projektovým potřebám.</p>

            </div>
        </div>
    </div>
</div>








<!-- Full Width Module -->
<div class="container mt-5">
    <div class="row">
        <div class="col">
            <div class="full-width-module">
                <h3>Zobrazení úkolů našeho týmu</h3>
                <table class="table">
                    <thead class="table-dark">
                        <tr>
                            <th>Úkol</th>
                            <th>Priorita</th>
                            <th>Stav</th>
                            <th>Přiděleno</th>
                            <th>Kategorie</th>

                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>PHP vývojářka</td>
                            <td>Střední</td>
                            <td>Probíhá</td>
                            <td>Ester</td>
                            <td>Backend</td>

                        </tr>
                        <tr>
                            <td>PHP vývojář</td>
                            <td>Střední</td>
                            <td>Probíhá</td>
                            <td>Tristan</td>
                            <td>Backend fdk.cz</td>

                        </tr>
                        <tr>
                            <td>Hlavní backendový vývojář</td>
                            <td>Střední</td>
                            <td>Probíhá</td>
                            <td>Ionno</td>
                            <td>Backend</td>

                        </tr>
                        <tr>
                            <td>Hlavní designerka & iOS vývoj</td>
                            <td>Vysoká</td>
                            <td>Probíhá</td>
                            <td>Pavla</td>
                            <td>Design</td>
                        </tr>
                        <tr>
                            <td>Vývoj iOS aplikace</td>
                            <td>Vysoká</td>
                            <td>Probíhá</td>
                            <td>Kristian</td>
                            <td>iOS</td>
                        </tr>
                        <tr>
                            <td>Integrační testování</td>
                            <td>Střední</td>
                            <td>Probíhá</td>
                            <td>Barča</td>
                            <td>Testování</td>

                        </tr>
                        <tr>
                            <td>Bezpečnostní audit</td>
                            <td>Vysoká</td>
                            <td>Probíhá</td>
                            <td>Míša</td>
                            <td>Bezpečnost</td>
                        </tr>
                        <tr>
                            <td>Frontendový vývoj</td>
                            <td>Vysoká</td>
                            <td>Probíhá</td>
                            <td>Aleš</td>
                            <td>Frontend</td>
                        </tr>
                        <tr>
                            <td>Konceptace</td>
                            <td>Vysoká</td>
                            <td>Probíhá</td>
                            <td>Martin</td>
                            <td>Analýza</td>
                        </tr>
                    </tbody>
                </table>
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
                            <p>Zachránit svět</p>
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
                            <p>Vývoj správce úkolů</p>
                        </div>
                    </div>
                    <!-- Done Column -->
                    <div class="task-column">
                        <h3><?php echo $translations['done'] ?><!--Done--></h3>
                        <div class="task-card">
                            <h4>Úkol  3</h4>
                            <p>Ano</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>







<?php include "./includes/footer.php" ?>

</body>
</html>
