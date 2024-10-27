/*show menu */
const showMenu = (toggleId, navId)=>{
    const toggle = document.getElementById(toggleId),
          nav= document.getElementById(navId)

    toggle.addEventListener('click', ()=>{
        //add show-menu class to nav menu
        nav.classList.toggle('show-menu')
        // add show-icon to show and hide menu icon
        toggle.classList.toggle('show-icon')
    })
}
showMenu('nav-toggle', 'nav-menu');
//zobrazeni veskereho skryteho textu

// Vybereme v�echny odkazy s t��dou .dropdown-link
const dropdownLinks = document.querySelectorAll('.dropdown-link');

// Vybereme konkr�tn� <h2> element, kde chceme m�nit text
const h2Element = document.querySelector('.headerName');

// P�id�me ud�lost click pro ka�d� odkaz
dropdownLinks.forEach(link => {
    link.addEventListener('click', function() {
        // Pokus�me se naj�t <span> uvnit� odkazu
        const spanElement = this.querySelector('span');
        
        // Zkontrolujeme, zda existuje <span>, pokud ne, vezmeme text z odkazu
        const newText = spanElement ? spanElement.textContent : this.textContent.trim();
        
        // Zm�n�me text v h2 s t��dou .headerName (ignorujeme <label> a ikonu)
        h2Element.childNodes[2].nodeValue = " " + newText;
        
        // Nech�me prohl�e� norm�ln� p�esm�rovat na URL uvedenou v href odkazu
    });
});

//Klikaci buton pro zobrazen� vse co je skryto a zpet
// Vybereme v�echny tabulky a tla��tka
const toggleButtons = document.querySelectorAll('.toggleTasksButton');
const taskTables = document.querySelectorAll('.taskTable');

// P�id�me ud�lost click na ka�d� tla��tko
toggleButtons.forEach((button, index) => {
    button.addEventListener('click', function() {
        // Najdeme odpov�daj�c� tabulku (index tla��tka odpov�d� indexu tabulky)
        const taskTableBody = taskTables[index].querySelector('tbody');
        const hiddenRows = taskTableBody.querySelectorAll('tr:nth-child(n+10)');

        // Zkontrolujeme, zda jsou aktu�ln� skryt� nebo zobrazen�
        if (hiddenRows[0].style.display === 'none' || hiddenRows[0].style.display === '') {
            // Zobraz�me v�echny ��dky
            hiddenRows.forEach(row => {
                row.style.display = 'table-row';
            });
            
            // Zm�n�me text tla��tka na "Skr�t v�e"
            button.innerHTML = 'Skr�t v�e <span class="las la-arrow-up"></span>';
        } else {
            // Skryjeme ��dky od �est�ho ��dku
            hiddenRows.forEach(row => {
                row.style.display = 'none';
            });
            
            // Zm�n�me text tla��tka zp�t na "Zobrazit v�e"
            button.innerHTML = 'Zobrazit v�e <span class="las la-arrow-right"></span>';
        }
    });
});
/*zobrazeni kolegove a kontakty*/
document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-button');

    toggleButtons.forEach(function(button) {
        button.addEventListener('click', function () {
            // Najdeme rodi�ovsk� prvek tla��tka, kter� obsahuje seznam koleg�
            const customerList = this.closest('.card').querySelector('.customer-list');

            if (customerList) {
                customerList.classList.toggle('show-all');

                // Zm�na textu tla��tka po kliknut�
                if (this.textContent.includes('Zobrazit v�e')) {
                    this.innerHTML = 'Skr�t v�e <span class="las la-arrow-right"></span>';
                } else {
                    this.innerHTML = 'Zobrazit v�e <span class="las la-arrow-right"></span>';
                }
            }
        });
    });
});