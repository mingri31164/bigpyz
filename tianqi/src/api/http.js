import axios from 'axios';

axios.get('http://110.41.64.229:8002/tem').then(res=>{
        console.log(res.data)
        console.log(res)
        console.log(typeof res.data)
        // const ans = JSON.parse(res.data)
        // console.log(typeof ans)
        // console.log(ans.data)
        console.log(res.data.code)
        console.log(res.data.dates)
        if(res.data.code === 200){
          const {dates,hei_his_temps,hei_temps,low_his_temps,low_temps,pre_hei_temps,pre_low_temps } = res.data.data;
          console.log(dates)
          console.log(hei_his_temps)
          console.log(hei_temps)
          console.log(low_his_temps)
          console.log(low_temps)
          console.log(pre_hei_temps)
          console.log(pre_low_temps)
        }

    })