<?php

require_once "include/db_connetion.php";
include "includes/settings.php";

$translations = include "translations/$language.php";

?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $translations['title'] ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

.task-board {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    padding: 20px 0;
}

.task-column {
    flex: 1 0 calc(33.333% - 20px);
    max-width: calc(33.333% - 20px);
    margin: 0 10px;
    margin-bottom: 20px;
}

.task-column h3 {
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
    margin-bottom: 20px;
    font-weight: bold;
    text-align: center;
}

.task-card {
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
}

.task-card h4 {
    margin-bottom: 5px;
    font-weight: bold;
}

.full-width-module {
    width: 100%;
    margin-bottom: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.sidebar-module {
    width: 100%;
    margin-bottom: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.footer {
    background-color: #222;
    color: #fff;
    padding: 30px 0;
    text-align: center;
    font-size: 14px;
}

.footer-links {
    list-style-type: none;
    padding: 0;
}

.footer-links li {
    margin-bottom: 10px;
}

.footer-links a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
}

.footer-links a:hover {
    color: #ccc;
}

.pc {
    display: none;
}

@media (max-width: 768px) {
    .task-column {
        flex: 1 0 calc(50% - 20px);
        max-width: calc(50% - 20px);
    }
    .tablet {
        display: none;
    }
}

@media (max-width: 576px) {
    .task-column {
        flex: 1 0 100%;
        max-width: 100%;
        margin: 0 auto;
    }
    .mobile {
        display: none;
    }
    .pc {
        display: block;
    }
}

    </style>
</head>
<body>
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
                Projekt pro potřeby jednoho unikátního týmu, ale otevřeno pro testování všem.
            </div>
        </div>
        <div class="col-md-9 col-12">
            <!-- Hlavní obsah -->
            <div class="full-width-module">
            <!--Vítejte v novém a jedinečném nástroji pro správu úkolů, který přináší revoluční 
            možnosti spolupráce a efektivity. 
            Tento nástroj je něčím, o čem jste dosud jen snili, ale teď je to skutečností, 
            kterou můžete okamžitě využít zdarma.-->
            Vítejte v revolučním nástroji pro správu úkolů! Náš task manager přináší rychlý a pružný způsob, 
            jak koordinovat práci Vašeho týmu. To, co bylo dříve pouze snem, se nyní stává skutečností. 
            A je navíc k dispozici zcela zdarma! 
            Zapomeňte na hranice spolupráce a přesuňte svůj tým do nové éry produktivity.
            </div>
        </div>
    </div>
</div>




    <!-- Main Content -->
    <div class="container mt-5">
        <div class="row">
            <div class="col-12">
                <div class="task-board">
                    <div class="task-column">
                        <h3>K provedení<!--To-Do--></h3>
                        <div class="task-card">
                            <h4>Úkol 1</h4>
                            <p>Vytvořit prezentaci pro klienta</p>
                        </div>
                        <div class="task-card">
                            <h4>Úkol 2</h4>
                            <p>Aktualizovat obsah webové stránky</p>
                        </div>
                    </div>
                    <div class="task-column">
                        <h3>V procesu<!--In Progress--></h3>
                        <div class="task-card">
                            <h4>Úkol 3</h4>
                            <p>Analyzovat výsledky marketingové kampaně</p>
                        </div>
                    </div>
                    <div class="task-column">
                        <h3>Hotovo<!--Done--></h3>
                        <div class="task-card">
                            <h4>Úkol  4</h4>
                            <p>Sehnat nástroj pro správu úkolů. Zdarma!</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>




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

                            <tr>
                                <td>Sehnat nástroj pro správu úkolů</td>
                                <td>Vysoká</td>
                                <td class="mobile">Dokončeno</td>
                                <td>Martin</td>
                                <td>Projekt</td>
                                <td class="tablet mobile">Barča</td>
                            </tr>

                          
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





    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <h4>O nás</h4>
                    <p>Lorem ipsum dolor sit amet. Ano, tento text tu chceme mít. Je to symbol něčeho co vzniká a mění se. Jediná konstanta v životě je změna.</p>
                </div>
                <div class="col-md-4">
                    <h4>Užitečné odkazy</h4>
                    <ul class="footer-links">
                        <li><a href="#">Domů</a></li>
                        <li><a href="#">O nás</a></li>
                        <li><a href="#">Služby</a></li>
                        <li><a href="#">Kontakt</a></li>
                    </ul>
                </div>
                <div class="col-md-4">
                    <h4>Kontaktuje nás:</h4> 
                    <p>eKultura z.s.</p>
                    <p>Email: info@div.cz</p>
                    <p>Phone: hmm, uvidíme</p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
