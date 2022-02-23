
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

function build_widgets(data){
    high_level_info(data)
    update_doughnutChart(data)
}

function high_level_info(data){
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

function update_doughnutChart(data){
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