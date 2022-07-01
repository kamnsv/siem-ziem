// sidebar
function hidesidebar() {
  const sidebar = document.getElementById('content');
  console.log(sidebar)
  sidebar.classList.add('hide');

}

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main-layout").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main-layout").style.marginLeft = "0";
} 

//main functions
function changeMenu(event) {
  const url = event.dataset.url;
  const menu = document.getElementById(event.dataset.menu);
  Array.from(document.querySelectorAll('.active')).forEach((el) => el.classList.remove('active'));
  event.classList.add('active');
  event.parentNode.classList.add('active');
  menu.classList.add('active');
  fetch(url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
     document.getElementById("main-layout").innerHTML = data;
    });
}

function putRule(event) {
  const params = new URLSearchParams([...new FormData(document.getElementById("form")).entries()]);
  const data = new URLSearchParams();
  const form = document.getElementById("form");
  const url = form.action;
  for (const pair of new FormData(form)) {
      data.append(pair[0], pair[1]);
  }
  fetch(url, {
      method: 'post',
      body: data,
    })
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      document.getElementById("main-layout").innerHTML = data;
    });
};
  
function postForm(event) {
  const params = new URLSearchParams([...new FormData(document.getElementById("form")).entries()]);
  const data = new URLSearchParams();
  const form = document.getElementById("form");
  const url = form.action;
  if (!form.checkValidity()){
    form.reportValidity()
  }
  else {
    for (const pair of new FormData(form)) {
        data.append(pair[0], pair[1]);
    }
    fetch(url, {
        method: 'post',
        body: data,
      })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        let myAlert = document.querySelector('.toast');
        let bsAlert = new bootstrap.Toast(myAlert);
        document.getElementById("toast_value").innerHTML = data;
        bsAlert.show();
      });
  }
};
  
function editRule(event) {
  const url = event.dataset.url;
  fetch(url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
     document.getElementById("main-layout").innerHTML = data;
    });
};

function selectObj(event) {
  const url = event.value;
  fetch(url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
     document.getElementById("main-layout").innerHTML = data;
    });
};

//cor deeprule 
function addExtraRows(obj) {
  var table = document.querySelector('#extra-table tbody');
  //var table = obj.parentNode.parentNode.parentNode;
  var length = table.rows.length - 1;
  var row=table.rows[length].cloneNode(true);
  row.classList.remove('d-none');
  for(var cell of row.cells) 
    {
      cell.innerHTML = cell.innerHTML.replaceAll("events-", "events-1");
      cell.innerHTML = cell.innerHTML.replaceAll(/selected="" value=/g, "value=");
      cell.innerHTML = cell.innerHTML.replaceAll(/text" value=".*"/g, 'text" value=');
    }
  table.insertBefore(row, table.firstElementChild.nextElementSibling);
 //table.prepend(row);
}

function addFilterRows(obj) {
  var table = document.querySelector('#extra-table tbody'); 
  //var table = obj.parentNode.parentNode.parentNode.parentNode;
  var length = table.rows.length - 1;
  var row=table.rows[length].cloneNode(true);
  row.classList.remove('d-none');
  row.value = "";
  for(var cell of row.cells) 
    {
      cell.innerHTML = cell.innerHTML.replaceAll("filter-", "filter-1");
      cell.innerHTML = cell.innerHTML.replaceAll(/selected="" value=/g, "value=");
      cell.innerHTML = cell.innerHTML.replaceAll(/text" value=".*"/g, 'text" value=');
    }
  table.insertBefore(row, table.firstElementChild.nextElementSibling);  
  //table.appendChild(row);
}

function removeExtraRow(obj) {
  var row = obj.parentNode.parentNode;
  var table = obj.parentNode.parentNode.parentNode;
  var length = table.rows.length;
  if (length == 2) {
    row.classList.add('d-none');
    for(var cell of row.cells) 
      {
      cell.innerHTML = cell.innerHTML.replaceAll(/selected="" value=/g, "value=");
      cell.innerHTML = cell.innerHTML.replaceAll(/text" value=".*"/g, 'text" value=');
      }
  } else {
    row.parentNode.removeChild(row);
  }
}

//nor rule
function addRegextraRows(obj) {
  var table = obj.parentNode.parentNode.parentNode;
  var length = table.rows.length - 1;
  var row=table.rows[length].cloneNode(true);
  row.classList.remove('d-none');
  row.value = "";
  for(var cell of row.cells) 
    {
      cell.innerHTML = cell.innerHTML.replaceAll("regex-", "regex-1");
      cell.innerHTML = cell.innerHTML.replaceAll(/selected="" value=/g, "value=");
      cell.innerHTML = cell.innerHTML.replaceAll(/text" value=".*"/g, 'text" value=');
    }
  table.appendChild(row);
}

//log rule
function addExtraLogs(obj) {
  //var table = obj.parentNode.parentNode.parentNode;
  var table = document.querySelector('#extra-table tbody');
  var length = table.rows.length - 1;
  var row=table.rows[length].cloneNode(true);
  row.classList.remove('d-none');
  for(var cell of row.cells) 
    {
      console.log(cell)
      cell.innerHTML = cell.innerHTML.replaceAll("logs-", "logs-1");
      cell.innerHTML = cell.innerHTML.replaceAll(/selected="" value=/g, "value=");
      cell.innerHTML = cell.innerHTML.replaceAll(/text" value=".*"/g, 'text" value=');
    }
  table.appendChild(row);
  return row;
}

//load table
function loadTable(url){
  fetch(url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      var oData = JSON.parse(data);
      editTable(oData);
    }) 
}

//search table
function searchRow() {
  var input, filter, table, tr, td, i, j, tds, ths, matched;
  var page = [];
  var pages = [];
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  tr = document.getElementsByTagName("tr");
  var count = 0;
  var page_count = 1;
  var page_max = document.getElementById("page_max").value;
  var page_number = 1;
  for (i = 1; i < tr.length; i++) {
    tds = tr[i].getElementsByTagName("td");
    ths = tr[i].getElementsByTagName("th");
    tr[i].style.display = "none";
    tr[i].setAttribute("data-page", 0);
    matched = false;
    if (ths.length > 0) {
      matched = true;
    }
    else {
      for (j = 0; j < tds.length; j++) {
        td = tds[j];
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          matched = true;
          break;
        }
      }
    }
    if (matched == true) {
      count++;
      pages.push(tr[i]);
      tr[i].setAttribute("data-page", page_number);
      page_count++;
      if (page_number == 1){
        tr[i].style.display = "";
      }
      if (page_count > page_max){
        tr[i].style.display = "";
        page_count = 1;
        page_number++;
      }
    }
    else {
        tr[i].style.display = "none";
    }
  }
  document.getElementById("table-count").textContent=count;
  document.getElementById("pages").textContent=page_number;
  document.getElementById("pages").dataset.page=page_number;
  document.getElementById("page").textContent=1;
  document.getElementById("page_next").dataset.page=2;
  document.getElementById("page_prev").dataset.page=0;
  document.getElementById("page_prev").classList.add('disabled');
  if (page_number == 1){
    document.getElementById("page_next").classList.add('disabled');
  }
  else{
    document.getElementById("page_next").classList.remove('disabled');
  }
}

//sort table
function sortTableByColumn(e, tableId, columnNumber) {
  console.log(columnNumber)
  var order = e.dataset.order;
  var tableElement=document.getElementById(tableId);
  var sorted = [].slice.call(tableElement.tBodies[0].rows).sort(function(a, b) {
      return (
        a.cells[columnNumber].textContent>b.cells[columnNumber].textContent?1:
        a.cells[columnNumber].textContent<b.cells[columnNumber].textContent?-1:
        0);
    });
  if (order == 'desc') {
    sorted.reverse();
    e.setAttribute("data-order", "inc");
  }
  else {
    e.setAttribute("data-order", "desc");
  }
  sorted.forEach(function(val, index) {
      tableElement.tBodies[0].appendChild(val);
  });
}

//paginator
function renderPaginator(e){
  var tableElement=document.getElementById(e);
  e.innerHTML = `
    <div class="border-top d-flex align-items-center justify-content-end p-2">
      Строк:
      <select 
        class="mx-2 form-control"
        style="width:60px"
        id="page_max" 
        onchange="searchRow()">
        <option value="25" selected=""> 
          25
        </option>
        <option value="50"> 
          50
        </option>
        <option value="100"> 
          100
        </option>
      </select>
      <span 
        class="mx-2"
        id="page">
        1 
      </span>
      из
      <span 
        class="mx-2"
        data-page="1"
        id="pages">
      </span>
      <a 
        class="btn btn-sm disabled btn-outline-secondary mx-2" 
        onclick="switchPage('prev')"
        id="page_prev"
        data-page="0">
        <i class="fas fa-angle-left"></i>
      </a>
      <a 
        class="btn btn-sm btn-outline-secondary" 
        onclick="switchPage('next')"
        id="page_next"
        data-page="2">
        <i class="fas fa-angle-right"></i>
      </a>          
    </div>
  `;
}

function switchPage(action) {
  var page_number, page;
  var tr = document.getElementsByTagName("tr");
  var pages = parseInt(document.getElementById("pages").dataset.page);
  var page_next = document.getElementById("page_next");
  var page_prev = document.getElementById("page_prev");
  if (action == 'next'){
    page_prev.classList.remove('disabled');
    page = page_next.dataset.page;
    page_next.dataset.page++;
    page_prev.dataset.page++;
  }
  else{
    page_next.classList.remove('disabled');
    page = page_prev.dataset.page;
    page_next.dataset.page--;
    page_prev.dataset.page--;
  }
  if (page_prev.dataset.page < 1){
    page_prev.classList.add('disabled');
  }
  else if (page_next.dataset.page > pages) {
    page_next.classList.add('disabled');
  }
  for (i = 1; i < tr.length; i++) {
    tr[i].style.display = "none";
    page_number = tr[i].dataset.page;
    if ( page == page_number ){
        tr[i].style.display = "";
    }
  }
  document.getElementById("page").textContent=page;
}

function postData() {
  const params = new URLSearchParams([...new FormData(document.getElementById("form")).entries()]);
  const data = new URLSearchParams();
  const url = document.getElementById("form").action;
  for (const pair of new FormData(form)) {
      data.append(pair[0], pair[1]);
  }
  fetch(url, {
      method: 'post',
      body: data,
      })
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      editTable(JSON.parse(data))
      searchRow();
    });
};


//table actions
function checkAllRow(e){
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var checked_count=document.getElementById('checked_count')
  main_panel.classList.add('d-none');
  panel.classList.remove('d-none');
  var tr = document.getElementsByTagName("tr");
  var count = 0;
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      if (e.checked){
        tr[i].children[0].children[0].children[0].checked = true;
        count++;
      }
      else{
        tr[i].children[0].children[0].children[0].checked = false;
        count == 0;
      }
    }
  }
  if (count == 0 ){
    panel.classList.add('d-none');
    main_panel.classList.remove('d-none');
  }  
  checked_count.textContent = count;
}

function checkRow(e){
  var main_panel=document.getElementById('main_panel');
  main_panel.classList.add('d-none');
  var panel=document.getElementById('panel');
  panel.classList.remove('d-none');
  var checked_count=document.getElementById('checked_count')
  if (checked_count){
    count = checked_count.textContent;
  }
  if (e.checked){
    count++;
  }
  else{
    count--;
  }
  if (count == 0 ){
    panel.classList.add('d-none');
    main_panel.classList.remove('d-none');
  }
  checked_count.textContent = count
}

function deleteRow(){
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  main_panel.classList.remove('d-none');
  panel.classList.add('d-none');
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      if ( check_box.checked == true){
        table.deleteRow(i);
        i--;
        fetch(url + check_box.value + "/del")
          .then((response) => {
            return response.text();
          })
          .then((data) => {
            let myAlert = document.querySelector('.toast');
            let bsAlert = new bootstrap.Toast(myAlert);
            document.getElementById("toast_value").innerHTML = data;
            bsAlert.show();
          });
      }
    }
  }
  searchRow();
  document.getElementById('check_allrow').checked = false;
}

function copyRow(){
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var body=table.getElementsByTagName('tbody')[0];
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  main_panel.classList.remove('d-none');
  panel.classList.add('d-none');
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      if ( check_box.checked == true){
        check_box.checked = false;
        fetch(url + check_box.value + "/copy")
          .then((response) => {
            return response.text();
          })
          .then((data) => {
            var oData = JSON.parse(data);
            let myAlert = document.querySelector('.toast');
            let bsAlert = new bootstrap.Toast(myAlert);
            insertRow(oData.doc, body)
            document.getElementById("toast_value").innerHTML = oData.text;
            bsAlert.show();
          });
      }
    }
  }
  document.getElementById('check_allrow').checked = false;
}

function syncRow(){
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  var selected_obj = document.getElementById("selected_obj");
  var obj = selected_obj.options[selected_obj.selectedIndex].text;
  main_panel.classList.remove('d-none');
  panel.classList.add('d-none');
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      diff = tr[i].children[3]
      if ( check_box.checked == true){
        diff.innerHTML = ''
        check_box.checked = false;
        fetch(url + check_box.value + "/sync/" + obj)
          .then((response) => {
            return response.text();
          })
          .then((data) => {
            let myAlert = document.querySelector('.toast');
            let bsAlert = new bootstrap.Toast(myAlert);
            document.getElementById("toast_value").innerHTML = data;
            bsAlert.show();
          });
      }
    }
  }
  document.getElementById('check_allrow').checked = false;
}

function syncRow(){
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  var selected_obj = document.getElementById("selected_obj");
  var obj = selected_obj.options[selected_obj.selectedIndex].text;
  main_panel.classList.remove('d-none');
  panel.classList.add('d-none');
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      diff = tr[i].children[3]
      if ( check_box.checked == true){
        diff.innerHTML = ''
        check_box.checked = false;
        fetch(url + check_box.value + "/sync/" + obj)
          .then((response) => {
            return response.text();
          })
          .then((data) => {
            let myAlert = document.querySelector('.toast');
            let bsAlert = new bootstrap.Toast(myAlert);
            document.getElementById("toast_value").innerHTML = data;
            bsAlert.show();
          });
      }
    }
  }
  document.getElementById('check_allrow').checked = false;
}

function checkNorRow(e){
  var myModal = new bootstrap.Modal(document.getElementById('Modal'))
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  var selected_obj = document.getElementById("selected_obj");
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      diff = tr[i].children[3]
      if ( check_box.checked == true){
        fetch(url + check_box.value + "/tax")
          .then((response) => {
            return response.text();
          })
          .then((data) => {
            myModal.show()
            document.querySelector(".modal-body").innerHTML = data;
          });
      }
    }
  }
}

function forceRow(){
  var url = document.getElementById('form').dataset.url;
  var table = document.getElementById('table');
  var main_panel=document.getElementById('main_panel');
  var panel=document.getElementById('panel');
  var tr = document.getElementsByTagName("tr");
  var selected_obj = document.getElementById("selected_obj");
  var obj = selected_obj.options[selected_obj.selectedIndex].text;
  main_panel.classList.remove('d-none');
  panel.classList.add('d-none');
  for (i = 1; i < tr.length; i++) {
    if (tr[i].style.display != "none"){
      check_box = tr[i].children[0].children[0].children[0];
      if ( check_box.checked == true){
        tr[i].children[3].innerHTML = `<span class="badge bg-secondary">Форс</span>` 
        check_box.checked = false;
        fetch(url + check_box.value + "/force")
          .then((response) => {
            if(response.status == '200'){
              return response.text();
            }
            else{
              return 'Ошибка форсирования';
            }
          })
          .then((data) => {
            let myAlert = document.querySelector('.toast');
            let bsAlert = new bootstrap.Toast(myAlert);
            document.getElementById("toast_value").innerHTML = data;
            bsAlert.show();
          });
      }
    }
  }
  document.getElementById('check_allrow').checked = false;
}
//test action

function testAction(e){
  const params = new URLSearchParams([...new FormData(document.getElementById("form")).entries()]);
  const data = new URLSearchParams();
  const form = document.getElementById("form"); 
  const url = form.action;
  for (const pair of new FormData(form)) {
      data.append(pair[0], pair[1]);
  }
  if (!form.checkValidity()){
    form.reportValidity()
  }
  else{
  var inner = e.innerHTML;
  e.classList.add('disabled');
  e.innerHTML=`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
  Загрузка...`;
  fetch(url, {
      method: 'post',
      body: data,
      })
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      e.innerHTML=inner;
      let myAlert = document.querySelector('.toast');
      let bsAlert = new bootstrap.Toast(myAlert);
      document.getElementById("toast_value").innerHTML = data;
      bsAlert.show();
      e.classList.remove('disabled');
    });
  }
}

//save table to csv
function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");
    for (var i = 0; i < rows.length; i++) {
        if(rows[i].style.display != 'none'){
          var row = [], cols = rows[i].querySelectorAll("td, th");
          for (var j = 0; j < cols.length; j++) 
              row.push(cols[j].innerText.replace(/(\n)/gm, ", "));
          console.log(row)
          csv.push(row.join(","));
        }
    }
    downloadCSV(csv.join("\n"), filename);
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
}

// click button for action
function clickButton(e){
  fetch(e.dataset.url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      let myAlert = document.querySelector('.toast');
      let bsAlert = new bootstrap.Toast(myAlert);
      document.getElementById("toast_value").innerHTML = data;
      bsAlert.show();
    });
}

// modal
function showModal(e){
  var myModal = new bootstrap.Modal(document.getElementById('Modal'))
  fetch(e.dataset.url)
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      myModal.show()
      document.querySelector(".modal-body").innerHTML = data;
    });
}


// show
function show_alert(text){
    let myAlert = document.querySelector('.toast');
    let bsAlert = new bootstrap.Toast(myAlert);
    document.getElementById("toast_value").innerHTML = text; 
    bsAlert.show();
}

// toggle load btn
function toggle_load_btn(e){
    e.classList.toggle('disabled');
    if (undefined == e.attributes['data-value']){
        var attr = document.createAttribute('data-value');
        attr.value = e.innerHTML;
        e.setAttributeNode(attr);
    }
    
    if (e.classList.contains('disabled'))
        e.innerHTML=`<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
  Загрузка...`;
    else
        e.innerHTML = e.attributes['data-value'].value;
    
}

//get data form
function get_data_form(e){
  const params = new URLSearchParams([...new FormData(e).entries()]);
  const data = new URLSearchParams();
  for (const pair of new FormData(form)) {
      data.append(pair[0], pair[1]);
  }
  return data;
}


// get opcae
function getOPCUA(e){
  const form = document.getElementById("form"); 
  const url = form.action;
  if (!form.checkValidity()){
    form.reportValidity();
    return;  
  }
    
  var data = get_data_form(form);
    
  toggle_load_btn(e);
   
  // Проверка соединения  
  if ('' == data.get('log')) {
      check_connecnt_opcua(data, function(text){
        toggle_load_btn(e);
        show_alert(text);
      });
  } 
  else  
  { // Запрос нод
      var name = data.get('log');
      check_connecnt_opcua(data, function(text){
        toggle_load_btn(e);
        if ('"OPCUA доступен"' != text){
            show_alert(text);
            return;
        }
          
        data.set('log', name);
        load_nodes_opcua(data, function(j){
            const id = 'nodes-'+data.get('ip').replace(/\./g,'_') + '-' + data.get('port');  
            document.getElementById("floatingLog").setAttribute("list", id);
            create_node_list(id, j);
            /*
            node = document.querySelector("#"+id+' option[value="'+data.get('log')+'"]');
            if (null != node)  {
                val = node.innerHTML;
                document.getElementById("floatingLogValue").innerHTML = val;
                show_alert('Значение ноды "'+data.get('log')+'": '+ val);
            } else show_alert('Нода "' +data.get('log')+ '" не найдена');
            */
            var valnode = findVal(j, data.get('log'));
            if (valnode != undefined){
                var node = document.querySelector("#"+id+' option[value="'+data.get('log')+'"]');
                var val = null;
                if (node != null) val = node.innerHTML;
                document.getElementById("floatingLogValue").innerHTML = val;
                show_alert('Значение ноды "'+data.get('log')+ (null == val ? 'не задано' : '": '+ val) );
            } else show_alert('Нода "' +data.get('log')+ '" не найдена');
            
            
            
            
          });
      });

  }
}

function findVal(object, key) {
    var value;
    Object.keys(object).some(function(k) {
        if (k === key) {
            value = object[k];
            return true;
        }
        if (object[k] && typeof object[k] === 'object') {
            value = findVal(object[k], key);
            return value !== undefined;
        }
    });
    return value;
}

//
function change_name_node(e){
    if (null == e.list) return;
    node = document.querySelector("#"+e.list.id+' option[value="'+e.value+'"]');
    if (null != node)  {
        val = node.innerHTML;
        val = format_code(val);
        document.getElementById("floatingLogValue").innerHTML = val;
    }
}

// format code
function format_code(val){
    if (null == val || undefined == val) val = '';
    else val = val.toString();
    val = val.replaceAll('<', '&lt;');
    val = val.replaceAll('>', '&gt;');
    val = val.replaceAll('\\r\\n', '<br>');
    return '<code>' + val + '</code>';
}

// create data list with nodes: value
function create_node_list(id, j){
    if (null != document.getElementById(id)) 
        document.getElementById(id).remove();
    const datalist = document.createElement("datalist");
    datalist.id = id;
    document.body.append(datalist);
    add_node_list(id, j);
}

// add nodes list recurced
function add_node_list(id, j, name){
    var dl = document.getElementById(id);
   
    for (i in j) 
        if ('value' == i) {
            var option = document.createElement('option');
            option.value = name;
            option.innerHTML = j[i];
            dl.appendChild(option);
        } else 
            add_node_list(id, j[i], i)
}


// check_connect
function check_connecnt_opcua(data, callback){
    var name = data.get('log');
    data.set('log', '');
    console.log('Проверка соединения ', data.get('ip')+':'+data.get('port')); 
    
    fetch('/test/get_opcua/', {
      method: 'post',
      body: data,
      })
    .then(response => {
      data.set('log', name); 
      return response.text();
    })
    .then(text => {
        callback(text);
    });
    
}

// Кэширование нод opcua
function caching_nodes_opcua(data, callback){
 
        var name = data.get('log');
        data.set('log', 'ns=1');
        const fname = '/static/yaml/opcua-'+data.get('ip')+'-'+data.get('port')+'.yml';

        console.log('Кэширование нод ', fname); 
        fetch('/test/get_opcua/', {
            method: 'post',
            body: data,
        })
        .then((r) => {
           data.set('log', name); 
           if (200 == r.status){
               callback();
           }
        });
    
}

// Запрос нод из кэша opcua
function load_nodes_opcua(data, callback){
  const fname = '/static/yaml/opcua-'+data.get('ip')+'-'+data.get('port')+'.yml'  
  fetch(fname, {
      method: 'get',
      })
    .then((response) => {
      
      if (404 == response.status){
          
          caching_nodes_opcua(data, function(){
              check_connecnt_opcua(data, function(text){
                  if ('"OPCUA доступен"' != text){
                    show_alert(text);
                    return callback();
                } else
                  load_nodes_opcua(data, callback);
              });
          });
          
          return null; 
      }
      
      return response.text();
        
    }).then(text => {
        if (null == text) return;
        callback(jsyaml.load(text));
    });
}


//Form log OPC AE

function change_protocol_log(e){
        if (null == e) return;
        if ('opcua' == e.value) {
            document.getElementById('SearchOpcaeNodes').classList.remove('d-none');
        } else {
            document.getElementById('SearchOpcaeNodes').classList.add('d-none');
        } 
}

document.addEventListener('DOMContentLoaded', function(){ 
    change_protocol_log(document.getElementById('protocol'));
    set_value_input_onclick_text_primary();
    fix_menu_hide();
});


function check_port(data){
    
  let port = document.getElementById('port');
  if (null == port) return show_alert('Ошибка, поле порта не найдено');  
  if ('' == data.get('ip') || '' == data.get('port')){ 
    if ('' == data.get('port')) {
      port.style.border = '1px solid red';  
      show_alert('Не обходимо указать порт подключения к источнику');
      
    }
    form.reportValidity();
    return;  
  } else  port.style.border = '';
  return true
}
// search nodes opcae
function search_opcae_nodes(e){
    /*
        Сначала данные ищем в кэше 
    */

  var name_nor = get_name_nor_for_ae();
  if ('' == name_nor) {
      show_alert('Установите правило нормализации OPC AE узлов');
      return
  }
  
  const form = document.getElementById("form"); 
  const url = '/test/get_opcua/';
  var data = get_data_form(form);
  
  // Проверка адреса  
  if (true !== check_port(data)) return;  
  
  toggle_load_btn(e);
   
  load_nodes_opcua(data, function(j){
          toggle_load_btn(e);
          
          const id = 'nodes-'+data.get('ip').replace(/\./g,'_') + '-' + data.get('port');  
          const name_nor = get_name_nor_for_ae();
          create_node_list(id, j);
          list = document.querySelectorAll('#'+id+' option')
          for (i of list) 
              if (i.innerHTML.indexOf('Protocol=(OPCAE)') > -1 && i.value.endsWith('.5000')){
                  console.log('#' + id + ' option[value="'+i.value.slice(0, -5)+'"]');
                  add_table_log(id, i.value, i.innerHTML, name_nor);
              }

  });


}

function get_name_nor_for_ae(){
    var table = document.querySelector('#extra-table tbody');
    var e = table.firstElementChild.nextElementSibling.querySelector('select');
    e.style.border = '' == e.value ? '1px solid red' : '';
    return e.value;
}

// add_table_log
function add_table_log(id, val, txt, name_nor){
  var row = addExtraLogs();
  var controls = row.querySelectorAll('.form-control');
  
  var name = val.slice(0, -5);  
  var item = document.querySelector('#' + id + ' option[value="'+val.slice(0, -5)+'"]')  
  
  var value = '';  
  if (null != item)
    value += item.innerHTML;
  value += ''==val ? txt : ' ' + txt;
    
  controls[0].value = name;
  controls[1].value = value;  
  var selector = row.querySelector('.form-select');
  selector.value = name_nor;
}

function set_value_input_onclick_text_primary(){
    var txts = document.querySelectorAll('.text-primary');
    for (txt of txts) {
        if (undefined == txt.attributes['data-target']) continue;
        txt.style.cursor = "pointer";
        txt.addEventListener('click', function(e){
            var t = e.target;
            if (undefined == t.attributes['data-target']) return;
            var val = t.attributes['data-set']
            val = undefined != val ? val.value : t.innerHTML.trim();
            var sel = t.attributes['data-target'].value;
            var inp = document.querySelector(sel);
            if (null == inp) return;
            inp.value = val;
        }) 
    }
}


function fix_menu_hide(){

    var items = document.querySelectorAll('#menu button');
    for (i of items)
        i.addEventListener('click', function(e){
            var sub = document.querySelectorAll('#menu div');
            var next = e.target.parentNode.querySelector('div');
            for (s of sub) 
                if (next != s)
                    s.classList.remove('show');
            
        });
}