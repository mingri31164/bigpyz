import axios from "axios";

export const getWater = async()=>{
let time = [],
    water = [];
  await axios.get('http://110.41.64.229:8002/preci').then(res=>{
   console.log(res.data);
  if(res.data.code === 200){
    const {dates,preci} = res.data.data;
    time = dates;
    water = preci;
  }
})


return {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: {
        color: '#999'
      }
    }
  },
 
  legend: {
    data: ['当日降水量']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: time,
      axisPointer: {
        type: 'shadow'
      }
    }
  ],
  yAxis: [
    {
      type: 'value',
      name: '降水量',
     
      // interval: 50,
      axisLabel: {
        formatter: '{value} ml'
      }
    },
    
  ],
  series: [
    {
      name: '当日降水量',
      type: 'bar',
      tooltip: {
        valueFormatter: function (value) {
          return value + ' ml';
        }
      },
      data:water
    },
   
  ]
};
}