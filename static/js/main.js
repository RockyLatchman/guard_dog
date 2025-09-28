

const accountModalHTML = `
      <div class="account-modal">
      <a href="" class="close">Close</a>
      <h3>Add account</h3>
       <form method="post" action="/account-manager">
          <input type="text" name="name" placeholder="Name" required>
          <input type="email" name="email" placeholder="E-mail" required>
          <input type="password" name="password" placeholder="Password" required>
          <input type="tel" name="mobile" placeholder="Mobile" required>
          <input type="text" name="category" placeholder="Category" required>
          <label>Due date</label>
          <input type="date" name="due_date" required>
          <input type="text" name="amount" placeholder="Amount" required>
          <textarea name="note" placeholder="Note"></textarea>
          <input type="submit" value="Add account">
       </form>
      </div> `;

const noteModalHTML = `
    <div class="note-modal">
      <a href="" class="close">Close</a>
      <h3>Notes</h3>
      <form method="post" action="/notes">
        <input type="text" name="title" placeholder="Title" required>
        <input type="email" name="category" placeholder="Category" required>
        <textarea name="note" placeholder="Note"></textarea>
        <input type="submit" value="Save note">
      </form>
    </div>`;

function createOverlay(){
  const overlay = document.createElement('div');
  overlay.setAttribute('class', 'overlay');
  return overlay;
}

function createTemplate(templateHTML){
  const template = document.createElement('template');
  template.innerHTML = templateHTML;
  return template.content;
}

function createModal(modalHTML){
  const modalTemplate = createTemplate(modalHTML);
  const overlay = createOverlay();
  overlay.appendChild(modalTemplate);
  document.body.appendChild(overlay);
}

function addAccountItem(){
  if (location.pathname == '/account-manager') {
    const addAccountItem = document.querySelector('#add-item');
    addAccountItem.addEventListener('click', (e) => {
        e.preventDefault();
        createModal(accountModalHTML);
    });
  }
}

function showPassword(){
  const password = document.querySelector('#password');
  password.addEventListener('click', (e) => {
       password.setAttribute('type', 'text');
  })
}

function editAccountItem() {
  const accountIds = document.querySelectorAll('[data-id]');
  const editAccountButton = document.querySelectorAll('.edit-item');
  editAccountButton.forEach((item) => {
      item.addEventListener('click', (e) => {
        fetch(`/account-manager/edit/${e.currentTarget.dataset.id}`)
          .then(response => response.json())
          .then(data => {
            //refactor this
               const date = new Date(data['account'][0]['due_date']);
               createModal(`
                  <div class="account-modal">
                      <a href="" class="close">Close</a>
                      <form method="post" action="/account-manager">
                         <input type="text" name="name" placeholder="Name" value="${data['account'][0]['name']}" required>
                         <input type="email" name="email" placeholder="E-mail" value="${data['account'][0]['email']}" required>
                         <label>Click password field to show password</label>
                         <input type="password" name="password" id="password" placeholder="Password" value="${data['account'][0]['password']}" required>
                         <input type="tel" name="mobile" placeholder="Mobile" value="${data['account'][0]['mobile']}" required>
                         <input type="text" name="category" placeholder="Category" value="${data['account'][0]['category']}" required>
                         <label>Due date</label>
                         <input type="text" name="due_date" value="${data['account'][0]['due_date']}" required>
                         <input type="text" name="amount" placeholder="Amount" value="${data['account'][0]['amount']}" required>
                         <textarea name="note" placeholder="Note">${data['account'][0]['note']}</textarea>
                         <input type="submit" value="Add account">
                      </form>
                     </div> `);
                     showPassword();
           })
           .catch(error => console.error('Error: ', error));
        });
     });
}

function addNote(){
   const addNoteButton = document.querySelector('#add-note');
   addNoteButton.addEventListener('click', (e) => {
      createModal(noteModalHTML);
   })
}

function editNote(){
  const editNoteButtons = document.querySelectorAll('.edit-note');
  editNoteButtons.forEach((edit_item) => {
    edit_item.addEventListener('click', (e) => {
      fetch(`/note/edit/${e.currentTarget.dataset.id}`)
        .then(response => response.json())
        .then(data => {
            //console.log(JSON.stringify(data['note']))
            createModal(`
              <div class="note-modal">
                <a href="" class="close">Close</a>
                <h3>Notes</h3>
                <form method="post" action="/notes">
                  <label>Title</label>
                  <input type="text" name="title" placeholder="title" value="${data['note'][0]['title']}" required>
                  <label>E-mail</label>
                  <input type="email" name="category" placeholder="category" value="${data['note'][0]['category']}" required>
                  <label>Note</label>
                  <textarea name="note" placeholder="Note">${data['note'][0]['note']}</textarea>
                  <input type="submit" value="Save note">
                </form>
              </div> `)
        })
        .catch(error => console.error('Error: ', error));
    })
  })
}


window.addEventListener('DOMContentLoaded', (e) => {
  addAccountItem();
  editAccountItem();
  addNote();
  editNote();
});
