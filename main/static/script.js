let today = new Date();
let get_year = today.getFullYear();
let get_month = today.getMonth() + 1;

let queryString = [];
let month_id;
let year_id;

$(document).ready(function () {
    console.log("docu ready");
    make_filter();

    for (let i = 0; i < 3; i++) {
        let id = "year" + i;
        $(document).on("click",
            "#" + id,
            function () {
                event.preventDefault();
                console.log(get_year - i + "" + "year filter selected");
                document.querySelectorAll(".selected_year").forEach(el => el.classList.remove("selected_year"));
                document.getElementById(id).classList.toggle("selected_year");
                year_id = get_year - i;
                if (month_id !== undefined) {
                    queryString.forEach(element => to_api(year_id, month_id, element));
                }

            });
    }

    for (let i = 1; i < 13; i++) {
        let id = "month" + i;
        $(document).on("click", "#" + id, function () {
            event.preventDefault();
            console.log(i + "month filter selected");
            document.querySelectorAll(".selected_month").forEach(el => el.classList.remove("selected_month"));
            document.getElementById(id).classList.toggle("selected_month");
            month_id = i;
            if (year_id !== undefined) {
                queryString.forEach(element => to_api(year_id, month_id, element));
            }
        });
    }
});


function make_filter() {
    let div0 = document.createElement("div");
    div0.id = 'year';
    let div1 = document.createElement("div");
    div1.id = 'month';

    for (let i = 0; i < 3; i++) {
        let filter_year = document.createElement("a");
        filter_year.appendChild(document.createTextNode(get_year - i + "년"));
        filter_year.id = "year" + i + "";
        div0.appendChild(filter_year);
    }
    for (let i = 1; i < 13; i++) {
        let filter_month = document.createElement("a");
        filter_month.appendChild(document.createTextNode(i + "월"));
        filter_month.id = "month" + i + "";
        div1.appendChild(filter_month);
    }

    $("#filter_div").append(div0);
    $("#filter_div").append(div1);

}

function to_table(json, subject) {
    let endDate = new Date(get_year - year_id, month_id, 0);
    console.log(get_year.toString() + "년 " + month_id.toString() + "월의 마지막 날짜는" + endDate.getDate() + "");

    let arrDate = [];
    let arrValue = [];
    let arrExpect = [];
    arrDate[0] = "날짜";
    arrValue[0] = subject;
    arrExpect[0] = "예측";


    for (let i = 0; i < endDate.getDate(); i++) {
        let date = i + 1;
        arrDate[i + 1] = month_id.toString() + "/" + date + "";
        arrExpect[i + 1] = "";

        if (json["value"][i] == null) {
            arrValue[i + 1] = "";
            continue;
        }
        arrValue[i + 1] = json["value"][i].toString();

    }

    const table = document.createElement("table");

    let tr0 = document.createElement("tr");
    let tr1 = document.createElement("tr");
    let tr2 = document.createElement("tr");

    for (let i = 0; i < arrDate.length; i++) {
        let td0 = document.createElement("td");
        td0.appendChild(document.createTextNode(arrDate[i]));

        let td1 = document.createElement("td");
        td1.appendChild(document.createTextNode(arrValue[i] + ""));

        let td2 = document.createElement("td");
        td2.appendChild(document.createTextNode(arrExpect[i]));

        tr0.appendChild(td0);
        tr1.appendChild(td1);
        tr2.appendChild(td2);

    }

    table.appendChild(tr0);
    table.appendChild(tr1);
    table.appendChild(tr2);

    return table;
}

function to_api(year, month, subject) {
    $("#" + subject).empty();
    let data = {
        subject: subject,
        year: year,
        month: month

    };

    $.ajax({
        url: '/post',
        data: JSON.stringify(data),
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        success: function (result) {
            let table = to_table(result, subject);
            table.id = "table_" + subject;
            table.className = subject;
            $("#" + subject).append(table);

        },
        error: function () {
            alert("Error!");
        }

    })

}

function add_subject() {
    let str_subject = $('#subject').val();
    $('#subject').val('');

    if (str_subject === "") {
        alert("검색어를 입력하세요");
        return;
    }

    if (queryString.includes(str_subject) === true) {
        return;
    }

    queryString.push(str_subject);
    let subject_elem = document.createElement("p");
    subject_elem.id = "subject_" + str_subject;
    subject_elem.className = str_subject;
    subject_elem.append(document.createTextNode(str_subject));

    $("#subject_div").append(subject_elem);
    let table_section = document.createElement("div");
    table_section.id = str_subject;
    $("#table_div").append(table_section);

    if (year_id !== undefined && month_id !== undefined) {
        to_api(year_id, month_id, str_subject);
    }

    $(document).on("click",
        "#subject_" + str_subject,
        function () {
            $("#subject_" + str_subject).remove();
            $("#" + str_subject).remove();
            let temp = [];
            for (let i = 0; i < queryString.length; i++) {
                if (queryString[i] !== str_subject) {
                    temp.push(queryString[i]);
                }
            }
            queryString = temp;
            console.log(temp.toString());

        });

}

function db_update() {
    $.ajax({
        url: '/update',
        method: 'GET'
    }).done(function () {
        alert("DB업데이트 요청완료!");
    }).fail(function (){
        alert("요청 실패!");
    })


}