<?php 

include "./includes/db_connection.php"; 
include "./includes/settings.php"; 

$translations = include "./assets/translations/$language.php";



?><!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?php echo $translations['index_title'] ?></title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">
</head>
<body>

<?php include "includes/header.php"; ?>

<!-- Navigation -->
<nav class="navbar border-bottom">
<button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">
           Logged user : 
          </h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">My profile</a>
              </li>
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">My tasks</a>
              </li>
              <form class="d-flex mt-3" method="post">
                <button>Log out</button>
            </form>
        </div>
        </div>


<!-- end of navigation -->

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
            <?php echo $translations['index_text'] ?>

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
