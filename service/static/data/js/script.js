  //init messaging data
  function update_ui(){
    let complete_messagesData = window.localStorage.getItem('received_messages')
    complete_messagesData = JSON.parse(complete_messagesData)
    msgCount_data = msgtype_counts(complete_messagesData)
    build_widgets(msgCount_data, complete_messagesData)
  }

  function msgtype_counts(complete_messagesData){
    chart_data = {
      "labels" : [],
      "data" : []
    }
    if(complete_messagesData != 'None'){
      _data = groupby_data(complete_messagesData)
      Object.keys(_data).forEach((x,d) =>{
        chart_data.labels.push(x)
        chart_data.data.push(_data[x].length)
      });
    }
    return chart_data;
  }

  function groupby_data(complete_messagesData){
    const x = complete_messagesData.conditions.reduce((group, task) => {
      group[task.task_name] = group[task.task_name] ?? [];
      group[task.task_name].push(task);
      return group;
    },{})
    return x
  }


  const cssColors = (color) => {
    return getComputedStyle(document.documentElement).getPropertyValue(color)
  }
  
  const getColor = () => {
    return window.localStorage.getItem('color') ?? 'cyan'
  }
  
  const colors = {
    primary: cssColors(`--color-${getColor()}`),
    primaryLight: cssColors(`--color-${getColor()}-light`),
    primaryLighter: cssColors(`--color-${getColor()}-lighter`),
    primaryDark: cssColors(`--color-${getColor()}-dark`),
    primaryDarker: cssColors(`--color-${getColor()}-darker`),
  }

function latencydata(serverLatency){
    data = [];
    localServerLatencyData = JSON.parse(window.localStorage.getItem('serverLatency'))
    console.log(localServerLatencyData, serverLatency)
    if(localServerLatencyData == null)
        {
            data.push(serverLatency)
            window.localStorage.setItem('serverLatency', JSON.stringify(data))
        }
    else
    {        
        data = JSON.parse(window.localStorage.getItem('serverLatency'))
        console.log("....",typeof(data));
        data.push(serverLatency)
        window.localStorage.setItem('serverLatency', JSON.stringify(data))
    }
    console.log(data)
    finalData = Object.values(data)
    let removedata = true;
    if(finalData.length > 10){
        while(finalData.length > 10){
            finalData.shift();
        }
        window.localStorage.setItem('serverLatency', JSON.stringify(finalData))
    }

    $(".dynamicsparkline").sparkline(data, {
        height: 20,
        width : 20,
        type: 'bar'});
}

function build_widgets(data, complete_messagesData){
    topLevel_WidgetsInfo(data)
    msgType_CountChart(data)
    drawTable(complete_messagesData)
}
function buildGridData(complete_messagesData){
  _data = [];
  if(complete_messagesData != undefined){
    complete_messagesData.conditions.forEach((element) => {

        minutes = 0;
        times = []
        startDT = ""
        endDT = ""
        element.conditions.forEach((eachStatus)=> {
          console.log(eachStatus)
          if(eachStatus.status_name === "PENDING"){
            startDT = eachStatus.status_datetime
            console.log("---->",startDT)
            times.push(eachStatus.status_datetime)
          }
          else if (eachStatus.status_name === "RECEIVED"){
            startDT = eachStatus.status_datetime
            console.log("---->",startDT)
            times.push(eachStatus.status_datetime)
          }

          if (eachStatus.status_name == "SUCCESS" || eachStatus.status_name == "FAIL"){
            endDT = eachStatus.status_datetime
          }
        })
        
        task = {"Id":element.task_id,
        "Type":element.task_name,
        "Info":element.message, 
        "TotalTime":"",
        "Status": element.conditions[element.conditions.length - 1].status_name, 
        "StartDateTime":startDT,
        "EndDateTime":endDT}
        _data.push(task)
    });
  }
  console.log(_data);
  return _data;
}


function topLevel_WidgetsInfo(data){
    console.log(data.labels)
    if(data != undefined || data != null){
        const initialValue = 0;
        const totalMessages = data.data.reduce(
            (previousValue, currentValue) => previousValue + currentValue,
            initialValue
          );        
        $('#total_msg').text(totalMessages);
        $('#total_email').text(data.labels.findIndex(element => element == "EMAIL") > -1 ? data.data[data.labels.findIndex(element => element == "EMAIL")] : 0);
        $('#total_sms').text(data.labels.findIndex(element => element == "SMS") > -1 ? data.data[data.labels.findIndex(element => element == "SMS")] : 0);
        $('#total_whatsapp').text(data.labels.findIndex(element => element == "WHATSAPP") > -1 ? data.data[data.labels.findIndex(element => element == "WHATSAPP")] : 0);
    }
}

//generate box plot
var messageTypeFormatter = function(cell, formatterParams, onRendered){
  if(cell.getValue() == "EMAIL"){
      return "<img src='static/data/images/Asset210.png'>";
  }
  else if(cell.getValue() == "SMS"){
      return "<img src='static/data/images/sms.png'>";
  }
  else{
      return "<img src='static/data/images/whatsapp.png'>";
  }
};

function drawTable(complete_messagesData){
  _data = buildGridData(complete_messagesData)
  //Table Constructor
  var table = new Tabulator("#example-table", {
    height:"311px",
    data : _data,
    colReorder: {
      realtime: false
  },
    columns:[
        {title:"Id", field:"Id", width:290},
        {title:"Type", field:"Type", width:90, formatter:messageTypeFormatter},
        {title:"Info", field:"Info", width:300},
        {title:"Task Start Date&Time", field:"StartDateTime", width:180},
        {title:"Task End Date&Time", field:"EndDateTime", width:180},
        {title:"Task Execution Time", field:"TotalTime", width:160},
        {title:"Status", field:"Status", width:100},
    ],
  });
}

function msgType_CountChart(data){
    const doughnutChart = new Chart(document.getElementById('doughnutChart'), {
        type: 'doughnut',
        data: {
          labels: data.labels,
          datasets: [
            {
              data: data.data,
              backgroundColor: [colors.primary, colors.primaryLighter, colors.primaryLight],
              hoverBackgroundColor: colors.primaryDark,
              borderWidth: 0,
              weight: 0.5,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          legend: {
            position: 'bottom',
          },
      
          title: {
            display: false,
          },
          animation: {
            animateScale: false,
            animateRotate: false,
          },
        },
      })

      return doughnutChart
}