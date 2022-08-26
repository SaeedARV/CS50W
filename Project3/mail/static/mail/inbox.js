document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


  document.querySelector("#compose-form").addEventListener('submit', function () {
    load_mailbox('sent');
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value
      })
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        load_mailbox('sent');
      })

  });
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);

      let table = document.createElement('table');
      let tbody = document.createElement('tbody');
      table.append(tbody);

      for (let i in emails) {
        let tr = document.createElement('tr');

        let td1 = document.createElement('td');
        let td2 = document.createElement('td');
        let td3 = document.createElement('td');

        td1.innerHTML = `${emails[i].sender}`;
        td2.innerHTML = `${emails[i].subject}`;
        td3.innerHTML = `${emails[i].timestamp}`;

        tr.append(td1);
        tr.append(td2);
        tr.append(td3);

        if (emails[i].read) {
          tr.setAttribute('class', 'read');
        }

        tr.onclick = function () {
          load_email(emails[i].id)
        }

        tbody.append(tr);

      }

      document.querySelector('#emails-view').append(table);
    });
}

function load_email(id) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);

      document.querySelector('#email-view').innerHTML = `
      <div><span class="bold">From:</span> ${email.sender} </div>
      <div><span class="bold">To:</span> ${email.recipients} </div>
      <div><span class="bold">Subject:</span> ${email.subject} </div>
      <div><span class="bold">Timestamp:</span> ${email.timestamp} </div>

      <hr>

      <div> ${email.body} </div>
      `

      if (email.read != true) {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
      }
    });


}