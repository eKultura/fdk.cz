<?php 
$title = null;
$description = null;
$category = null;
$priority = null;
$assigned = null;

include './includes/db_connection.php';

//GETTING VALUES FROM FOMR INTO VARIABILES
if(array_key_exists('send', $_POST)){
	$title = $_POST['title'];
	$description = $_POST['description'];
	$category = $_POST['category'];
	$priority = $_POST['priority'];
	$assigned = $_POST['assigned'];

    
    
    //INSERTING VALUES INTO DATABASE
    //EXEPTION
    try
    {
    $sql = $pdo->prepare("INSERT INTO `FDK_tasks` (title, description, category, priority, assigned) VALUES (?,?,?,?,?)");
    $sql->execute([$title, $description, $category_id, $priority, $assigned]);
    echo "Záznam byl úspěšně vložen!";
}

catch (PDOException $e) {
    echo "Chyba: " . $e->getMessage();
}

}


?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Document</title>
	 <!-- BOOTSTRAP -->
	 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.3/assets/css/docs.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <link href="https://fdk.cz/assets/style.css" rel="stylesheet">
    <link rel="stylesheet" href="css/index.css">
</head>
<body>
	<!-- ADD TASKS -->
    <div id="add-tasks" class="container-md">
        <form action="" method="post">
            <div class="add-task text-center">
                <label for="title">Jméno úkolu</label>
                <input id="title" name="title" type="text">

                <label for="description">Popis úkolu</label>
                <textarea name="description"></textarea>

                <label for="category">Kategórie:</label>
                <select name="category" id="category">
                    <option value="1">Frontend</option>
                    <option value="2">Backend</option>
                    <option value="3">Testovaní</option>
                    <option value="4">Databáze</option>
                    <option value="5">Server</option>
                    <option value="6">IOS</option>
                    <option value="7">Android</option>
                </select>

                <label for="priority">Priorita</label>
                <select name="priority" id="priority">
                    <option value="nizka">Nízka</option>
                    <option value="stredna">Střední</option>
                    <option value="vysoka">Vysoká</option>
                </select>

                <label for="assigned">Přiradiť</label>
                <select name="assigned" id="assigned">
						<option value="nikto">nikto</option>
					<option value="martin">martin</option>
					<option value="tristan">tristan</option>
					

                </select>

			<button type="submit" name="send">přidat</button>
            </div>
        </form>
    </div>
</body>
</html>