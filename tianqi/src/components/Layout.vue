<script setup>
import {ref,onBeforeMount} from 'vue'
import {getTem} from '../option/temperature.js';
import { getWater } from '../option/water.js';
import { getPre } from '../option/precipitation.js';
import Echarts from './Echarts.vue'

const tem =ref(null)
const precipitation = ref(null)
const water = ref(null)
onBeforeMount(()=>{
   getTem().then(data=>{
    tem.value = data; 
   })
   getPre().then(data=>{
    precipitation.value = data;
  })
  getWater().then(data=>{
    water.value = data;
  })

})

const TemWidth = ref('70.25rem');
const TemHeight = ref('32.0000rem');
console.log(tem.value);
const waterWidth = ref('25.25rem');
const waterHeight = ref('17.0000rem');

const PreWidth = ref('25.25rem');
const PreHeight = ref('17.0000rem');

const ldb = async()=>{
  tem.value = null;
  await getPre().then(data=>{
    tem.value = data;
  })
  console.log(tem.value);
}
</script>

<template>
 <div class="con">
  <div class="header">桂林市xx年天气数据统计   
  </div>
   
 
 <div id="box">
  <div class="main-left" style="margin-left: 1%;">
        <!--条形图-->
        <div class="border-container" >        
        <Echarts v-if="water" :dataSource="water" :canvasWidth="waterWidth" :canvasHeight="waterHeight"></Echarts>
        <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
        <!--折线图-->
        <div class="border-container">    
            <Echarts v-if="precipitation" :dataSource="precipitation" :canvasWidth="PreWidth" :canvasHeight="PreHeight"></Echarts> 
            <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
   

    </div>

    <div class="main-middle">
       
        <!-- <div class="no">
            <div class="no-hd">
                <ul>
                    <li>1211</li>
                    <li>1045</li>
                </ul>
            </div>
            <div class="no-bd">
                <ul>
                    <li>毕业总人数</li>
                    <li>就业总人数</li>
                </ul>
            </div>
        </div> -->

   
        <div class="border-container">
 
            <div id="main" style="width:60.4583rem;padding: 1.0417rem;">
              <div style="height: 2.1000rem;">
               <button @click="ldb()"> ldb</button>
              </div>
              <Echarts v-if="tem" :dataSource="tem" :canvasWidth="TemWidth" :canvasHeight="TemHeight"></Echarts>
            </div>
           
            <span class="top-left border-span"></span>
            <span class="top-right border-span"></span>
            <span class="bottom-left border-span"></span>
            <span class="bottom-right border-span"></span>
        </div>
    </div>

    <!-- <div class="main-right">

        <div class="border-container">        
            <div id="zhu" class="boxsize"></div> 
            <span class="top-left border-span"></span>
                <span class="top-right border-span"></span>
                <span class="bottom-left border-span"></span>
                <span class="bottom-right border-span"></span>
            </div>
         
            <div class="border-container">    
                <div id="liu" class="boxsize"></div> 
                <span class="top-left border-span"></span>
                <span class="top-right border-span"></span>
                <span class="bottom-left border-span"></span>
                <span class="bottom-right border-span"></span>
            </div>
        
        
    </div> -->
 </div>
 </div>
  
</template>

<style scoped>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

li {
    list-style: none;
}
.con{
  display: flex;
  flex-direction: column;
}
.header{
 height: 6.25rem;
 position: relative;
 padding-top: 13px;
 font-size: 36px;
 color: #ffffff;
 text-align: center;
 background: url(../assets/bg.png) top center no-repeat;
}
#box{
  flex: 1;
  display: flex;
  flex-direction: row
}
.border-container {
 position: relative;
 margin-top: 15px;
 padding: 10px;

 border: 1px solid rgba(255,255,255,.15);
box-shadow: inset 0 0 50px rgba(255,255,255,.1),0 0 5px rgba(0,0,0,.3)
}
.border-container span.top-left {
 top: -2px;
 left:-2px;
 border-top: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.top-right {
 top:-2px;
 right:-2px;
 border-top: 2px solid #54dcf2;
 border-right:2px solid #54dcf2;
}

.border-container span.bottom-left {
 bottom: -2px;
 left: -2px;
 border-bottom: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.bottom-right {
 bottom: -2px;
 right: -2px;
 border-bottom: 2px solid #54dcf2;
 border-right: 2px solid #54dcf2;
}
.main-left,
.main-right{
 float: left;
 width: 26%;
 height: 700px;
 padding: 0 10px;
}
.main-middle{
  padding: 0 10px;
  flex: 1;
  margin-right: 39px;
}
.boxsize{
  width: 15.625rem;
  height:16.8167rem;
}
.border-container span.border-span {
 display: block;
 position: absolute;
 width:20px;
 height: 20px; opacity: .5
}

.border-container span.top-left {
 top: -2px;
 left:-2px;
 border-top: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.top-right {
 top:-2px;
 right:-2px;
 border-top: 2px solid #54dcf2;
 border-right:2px solid #54dcf2;
}

.border-container span.bottom-left {
 bottom: -2px;
 left: -2px;
 border-bottom: 2px solid #54dcf2;
 border-left: 2px solid #54dcf2;
}

.border-container span.bottom-right {
 bottom: -2px;
 right: -2px;
 border-bottom: 2px solid #54dcf2;
 border-right: 2px solid #54dcf2;
}
.name-title{
 font-size:16px; font-weight: bolder;
 color: #00ffff;
}

/* @font-face{font-family:electronicFont;src:url(DS-DIGI-1.TTF)}
.number {
 font-size: 72px; 
 color: #0e94ea;  
 font-family:electronicFont; 
 font-weight: bold;
} */

.no {
  background: rgba(101, 132, 226, 0.1);
  padding: 0.1875rem;
  height: 100px;
  margin-top: 10px;
}

.no .no-hd {
  position: relative;
  border: 1px solid rgba(25, 186, 139, 0.17);
}

.no .no-hd::before {
  content: "";
  position: absolute;
  width: 30px;
  height: 10px;
  border-top: 2px solid #02a6b5;
  border-left: 2px solid #02a6b5;
  top: 0;
  left: 0;
}

.no .no-hd::after {
  content: "";
  position: absolute;
  width: 30px;
  height: 10px;
  border-bottom: 2px solid #02a6b5;
  border-right: 2px solid #02a6b5;
  right: 0;
  bottom: 0;
}

.no .no-hd ul {
  display: flex;
}

.no .no-hd ul li {
  position: relative;
  flex: 1;
  text-align: center;
  height: 50px;
  line-height: 62px;
  font-size: 24px;
  color: #ffeb7b;
  padding: 0.05rem 0;
  font-family: electronicFont;
  font-weight: bold;
}

.no .no-hd ul li:first-child::after {
  content: "";
  position: absolute;
  height: 50%;
  width: 1px;
  background: rgba(255, 255, 255, 0.2);
  right: 0;
  top: 25%;
}

.no .no-bd ul {
  display: flex;
}

.no .no-bd ul li {
  border: none;
  flex: 1;
  height: 50px;
  line-height: 50px;
  text-align: center;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
  padding-top: 0.125rem;
}


</style>
