<?php
session_start();

// Odstranění všech session proměnných
session_unset();

// Zničení session
session_destroy();

// Přesměrování na přihlašovací stránku nebo na domovskou stránku
header("Location: /?success=logout");
exit;
?>
