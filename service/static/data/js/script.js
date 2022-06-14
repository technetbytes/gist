let tabulatorGrid;
const random = (max = 100) => {
  return Math.round(Math.random() * max) + 20
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

const randomData = () => {
  return [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,,0,0,0,0,0,0,0,0,0,
  ]
}

const activeUsersChart = new Chart(document.getElementById('messagesBarChart'), {
  type: 'bar',
  data: {
    labels: [...randomData()],
    datasets: [
      {
        data: [...randomData()],
        label: "WhatsApp",
        borderColor: "#3cba9f",
        backgroundColor: "#71d1bd",
        borderWidth:2
      }, { 
        data: [...randomData()],
        label: "SMS",
        borderColor: "#ffa500",
        backgroundColor:"#ffc04d",
        borderWidth:2
      }, { 
        data: [...randomData()],
        label: "E-mail",
        borderColor: "#c45850",
        backgroundColor:"#d78f89",
        borderWidth:2
      }
    ]
   
  },
  options: {
    scales: {
       yAxes: [
        {
          display: false,
          gridLines: false,
          stacked: true 
        },
      ],
      xAxes: [
        {
          display: false,
          gridLines: false,
          stacked: true,
        },
      ],
      ticks: {
        padding: 10,
      },
    },
    cornerRadius: 2,
    maintainAspectRatio: false,
    legend: {
      display: true,
      position: 'bottom'
    },
    tooltips: {
      mode:'x'
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
  },
})

  //init messaging data
  function initUIData(){
    let complete_messagesData = window.localStorage.getItem('received_messages')
    complete_messagesData = JSON.parse(complete_messagesData)
    msgTypeCount_data = build_msgtype_counts(complete_messagesData)
    window.localStorage.setItem('msgTypeCount_data', JSON.stringify(msgTypeCount_data))
    build_widgets(msgTypeCount_data, complete_messagesData)
  }

  //Build Message Type Count Working
  function build_msgtype_counts(complete_messagesData){
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

  //GroupBy Data for Message Type Count Working
  function groupby_data(complete_messagesData){
    const x = complete_messagesData.conditions.reduce((group, task) => {
      group[task.task_name] = group[task.task_name] ?? [];
      group[task.task_name].push(task);
      return group;
    },{})
    return x
  }

  //GroupBy for Quick View Data not in use
  function groupby_quickViewData(quick_view_data){
    result = quick_view_data.reduce(function (r, a) {
          r[a.task_name] = r[a.task_name] || [];
          r[a.task_name].push(a);
          return r;
      }, Object.create(null));
      return result
  }

  function latencyData(serverLatency){
    data = [];
    localServerLatencyData = JSON.parse(window.localStorage.getItem('serverLatency'))
    //console.log(localServerLatencyData, serverLatency)
    if(localServerLatencyData == null)
        {
            data.push(serverLatency)
            window.localStorage.setItem('serverLatency', JSON.stringify(data))
        }
    else
    {        
        data = JSON.parse(window.localStorage.getItem('serverLatency'))
        data.push(serverLatency)
        window.localStorage.setItem('serverLatency', JSON.stringify(data))
    }
    //console.log(data)
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
    _data = buildGridData(complete_messagesData)
    drawTable()
  }

  function updateWidgetsUsingQuickViewData(quick_view_data){
    
  previous_MsgTypeCount_Data = JSON.parse(window.localStorage.getItem('msgTypeCount_data'))
  quick_data = JSON.parse(quick_view_data);
  quick_data = quick_data.sort((itemA, itemB) => itemA.task_id - itemB.task_id)
  
  //Step 1. Reduce By Task Name
  result = quick_data.reduce(function (r, a) {
            r[a.task_name] = r[a.task_name] || [];
            r[a.task_name].push(a);
            return r;
        }, Object.create(null));
  
  //Step 2. Create manage data with Labels and data properties
  chart_data = {"labels" : [], "data" : []}
  Object.keys(result).forEach((x,d) =>{
    chart_data.labels.push(x)
    inner_data = {}
    inner_data[x] = result[x].reduce(function (r, a) {
                    r[a.task_id] = r[a.task_id] || [];
                    r[a.task_id].push(a);
          return r;
      }, Object.create(null))
     chart_data.data.push(inner_data)
  });
  
  //Step 3.
  Object.entries(chart_data.data).forEach((dataA,dataIndex) =>{
    s = chart_data.data[dataIndex]
    c = s
      Object.keys(c).forEach((firstKey) =>{
        Object.entries(c).forEach((ss,ss1) => {
            _temp1 = c[firstKey]
            Object.keys(_temp1).forEach((eachKey)=>{                
                failSuccessDataItem = []
                pendingReceivedStartedDataItem = []                
              _temp1[eachKey].forEach((eachDataItem,index_) => {
                //Check for SUCCESS & FAIL					
                if(eachDataItem.status == 'SUCCESS' || eachDataItem.status == 'FAIL'){
                  failSuccessDataItem.push(eachDataItem);
                }
                else{
                  //Check for PENDING, RECEIVED & STARTED
                  pendingReceivedStartedDataItem.push(eachDataItem);
                }
              })
              
              if(failSuccessDataItem.length >= 1){
                //its mean's there is fail or success data item exist in the list
                //we dont need to do anything, simple set the list object to the _temp1[eachKey]
                _temp1[eachKey] = failSuccessDataItem
              }
              else if(pendingReceivedStartedDataItem.length > 0) {
                //we first check STARTED status, followed by RECEIVED and in the end PENDING
                //and remove the remain data items.
                let i = pendingReceivedStartedDataItem.length;
                
                isStartedFound = false;
                isReceivedFound = false;
                for(x=i-1;x>=0;x--){
                  //console.log("X", x)
                  if(pendingReceivedStartedDataItem[x].status == 'STARTED'){
                    isStartedFound = true;							
                  }
                  else if(pendingReceivedStartedDataItem[x].status == 'RECEIVED'){
                    isReceivedFound = true;
                  }
                }
                if(isStartedFound || isReceivedFound){
                  if(isStartedFound){
                    //using reverse looping
                    while(i--){
                      if(pendingReceivedStartedDataItem[i].status != 'STARTED'){
                        pendingReceivedStartedDataItem.splice(i,1)
                      }
                    }
                  }
                  else{
                    //using reverse looping					
                    while(i--){                      
                      if(pendingReceivedStartedDataItem[i].status != 'RECEIVED'){
                        pendingReceivedStartedDataItem.splice(i,1)
                      }
                    }
                  }
                  _temp1[eachKey] = pendingReceivedStartedDataItem
                }
                else{
                  _temp1[eachKey] = pendingReceivedStartedDataItem
                }
              }              
            })
          })
    })
  })

  data2 = {}
  chart_data.data.forEach((xx,indexX) => {
    Object.keys(xx).forEach((px,index) => {
      data2[px.toUpperCase()] = Object.keys(xx[px]).length
    })
  })
  
  if(previous_MsgTypeCount_Data.labels.findIndex(element => element == "EMAIL") > -1 ){
    let index = previous_MsgTypeCount_Data.labels.findIndex(element => element == "EMAIL");
    emailCount = previous_MsgTypeCount_Data.data[index];    
    if(data2.hasOwnProperty("EMAIL")){
      emailCount = emailCount + parseInt(data2["EMAIL"])
    }
    previous_MsgTypeCount_Data.data[index] = emailCount;
  }
  if(previous_MsgTypeCount_Data.labels.findIndex(element => element == "SMS") > -1 ){
    let index = previous_MsgTypeCount_Data.labels.findIndex(element => element == "SMS");
    smsCount = previous_MsgTypeCount_Data.data[index];    
    if(data2.hasOwnProperty("SMS")){
      smsCount = smsCount + parseInt(data2["SMS"])
    }
    previous_MsgTypeCount_Data.data[index] = smsCount;
  }
  if(previous_MsgTypeCount_Data.labels.findIndex(element => element == "WHATSAPP") > -1 ){
    let index = previous_MsgTypeCount_Data.labels.findIndex(element => element == "WHATSAPP");
    whatsappCount = previous_MsgTypeCount_Data.data[index];    
    if(data2.hasOwnProperty("WHATSAPP")){
      whatsappCount = whatsappCount + parseInt(data2["WHATSAPP"])
    }
    previous_MsgTypeCount_Data.data[index] = whatsappCount;
  }
  window.localStorage.setItem('msgTypeCount_data', JSON.stringify(previous_MsgTypeCount_Data))
  topLevel_WidgetsInfo(previous_MsgTypeCount_Data)
  msgType_CountChart(previous_MsgTypeCount_Data)
  message_Pulse_Count(data2)
}

function buildGridData(complete_messagesData){
  _data = [];
  if(complete_messagesData != undefined){
    minutes = 0;
    times = []
    calculatedTime = -1
    startDT = ""
    endDT = ""
    complete_messagesData.conditions.forEach((element) => {
        element.conditions.forEach((eachStatus)=> {
          //console.log(eachStatus)
          if(eachStatus.status_name == "PENDING"){
            startDT = eachStatus.status_datetime
            times.push(eachStatus.status_datetime)
          }
          else if (eachStatus.status_name == "RECEIVED"){
            startDT = eachStatus.status_datetime
            times = [] //clear the list to Pending Status conflict 
            times.push(eachStatus.status_datetime)
          }
          if (eachStatus.status_name == "SUCCESS" || eachStatus.status_name == "FAIL"){
            endDT = eachStatus.status_datetime
            //note the timing in either case
            times.push(eachStatus.status_datetime)
          }
        })
        
        //if two datetime exist in the list then perform subtraction (last-datetime - start-datetime)
        if(times.length == 2){
          calculatedTime = Math.abs(new Date(times[1]) - new Date(times[0])) / 60000;
        }

        task = {"Id":element.task_id,
        "Type":element.task_name,
        "Info":element.message, 
        "TotalTime": calculatedTime.toFixed(6),
        "Status": element.conditions.length > 0 ? element.conditions[element.conditions.length - 1].status_name : "WAITING", 
        "StartDateTime":startDT,
        "EndDateTime":endDT}
        _data.push(task)
    });
  }
  return _data;
}

function topLevel_WidgetsInfo(data){
    //console.log(data.labels)
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
      return "<img src='static/data/images/email_icon.png'>";
  }
  else if(cell.getValue() == "SMS"){
      return "<img src='static/data/images/sms_icon.png'>";
  }
  else{
      return "<img src='static/data/images/whatsapp_icon.png'>";
  }
};

$(document).ready(function() {
  $("#btnSubmit").click(function(){
      alert("button");
      //var selectedRows = $("#example-table").Tabulator("getSelectedRows").length;      
      console.log("sfffaf",table.data);
  }); 
});

function drawTable(){  
  //Table Constructor
  tabulatorGrid = new Tabulator("#example-table", {
    height:"311px",
    data : _data.reverse(),
    columns:[
        {title:"Id", field:"Id", width:290},
        {title:"Type", field:"Type", width:90, align:"center",formatter:messageTypeFormatter},
        {title:"Info", field:"Info", width:260},
        {title:"Task Start Date & Time", field:"StartDateTime", width:200},
        {title:"Task End Date & Time", field:"EndDateTime", width:200},
        {title:"Exec Time Mins.", field:"TotalTime", width:160},
        {title:"Status", field:"Status", width:80},
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

const message_Pulse_Count = (data2) => {
 const isoStr = new Date().toISOString();
  if(data2.hasOwnProperty("WHATSAPP") && data2.hasOwnProperty("SMS") && data2.hasOwnProperty("EMAIL")){
  activeUsersChart.data.datasets[0].data.push({x:isoStr, y:data2["WHATSAPP"]})
  activeUsersChart.data.datasets[0].data.splice(0, 1)
  activeUsersChart.data.datasets[1].data.push({x:isoStr, y:data2["SMS"]})
  activeUsersChart.data.datasets[1].data.splice(0, 1)
  activeUsersChart.data.datasets[2].data.push({x:isoStr, y:data2["EMAIL"]})
  activeUsersChart.data.datasets[2].data.splice(0, 1)
  }else if(data2.hasOwnProperty("WHATSAPP") && data2.hasOwnProperty("SMS")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:data2["WHATSAPP"]})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:data2["SMS"]})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }else if(data2.hasOwnProperty("WHATSAPP") && data2.hasOwnProperty("EMAIL")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:data2["WHATSAPP"]})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:data2["EMAIL"]})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }else if(data2.hasOwnProperty("SMS") && data2.hasOwnProperty("EMAIL")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:data2["SMS"]})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:data2["EMAIL"]})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }
  else if(data2.hasOwnProperty("SMS")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:data2["SMS"]})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }
  else if(data2.hasOwnProperty("EMAIL")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:data2["EMAIL"]})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }
  else if(data2.hasOwnProperty("WHATSAPP")){
    activeUsersChart.data.datasets[0].data.push({x:isoStr, y:data2["WHATSAPP"]})
    activeUsersChart.data.datasets[0].data.splice(0, 1)
    activeUsersChart.data.datasets[1].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[1].data.splice(0, 1)
    activeUsersChart.data.datasets[2].data.push({x:isoStr, y:0})
    activeUsersChart.data.datasets[2].data.splice(0, 1)
  }
  activeUsersChart.update()
}