<script setup lang="ts">
import { ref } from "vue";

const question = ref("");

const answer = ref("暂无回答");

const asking = ref(false);

const timeline = ref([
  {
    time: 0,
    text: "课程开始"
  },
  {
    time: 10,
    text: "今天学习人工智能基础"
  },
  {
    time: 30,
    text: "介绍神经网络结构"
  },
  {
    time: 60,
    text: "介绍 Transformer 模型"
  }
]);

const currentTime = ref(0);

// PPT mock数据
const slides = ref([
  {
    id: 1,
    title: "人工智能基础"
  },
  {
    id: 2,
    title: "神经网络结构"
  },
  {
    id: 3,
    title: "Transformer模型"
  }
]);


const currentSlide = ref(1);





function play(time: number) {
  currentTime.value = time;
}

function formatTime(time: number) {
  const m = Math.floor(time / 60);
  const s = time % 60;

  return `${m}:${s.toString().padStart(2, "0")}`;
}
async function ask(){

  if(!question.value.trim()){
    return;
  }

  asking.value=true;


  setTimeout(()=>{

    answer.value =
      "这是一个模拟回答：" + question.value;


    question.value="";

    asking.value=false;


  },800);

}

</script>


<template>
  <section>

<h1>课程详情</h1>


<div class="layout">


<!-- 左侧视频和时间轴 -->

<div class="main">


<div class="video-box">
  模拟视频播放区域
</div>


<h2>字幕</h2>

<p>
当前时间：
{{ formatTime(currentTime) }}
</p>


<div class="subtitle">

{{
timeline.find(
 item => item.time <= currentTime
)?.text
|| "暂无字幕"
}}

</div>



<h2>时间轴</h2>


<div
v-for="item in timeline"
:key="item.time"
class="timeline-item"
:class="{activeTime:item.time===currentTime}"
@click="play(item.time)"
>

{{formatTime(item.time)}}

-

{{item.text}}

</div>


</div>




<!-- 右侧区域 -->

<div class="side">


<h2>PPT</h2>


<div
v-for="slide in slides"
:key="slide.id"
class="slide"
:class="{active: currentSlide===slide.id}"
@click="currentSlide=slide.id"
>

第{{slide.id}}页：

{{slide.title}}

</div>



<h2>问答</h2>


<input
  v-model="question"
  placeholder="请输入问题"
/>


<button @click="ask">

  {{ asking ? "思考中..." : "提问" }}

</button>


<div class="answer">

  {{ answer }}

</div>


</div>



</div>


</section>
</template>


<style scoped>

.video-box {
  height: 200px;
  background: #eee;
  display:flex;
  align-items:center;
  justify-content:center;
}


.subtitle {
  margin:20px 0;
  padding:20px;
  border:1px solid #ddd;
}


.timeline-item {
  padding:10px;
  cursor:pointer;
}


.timeline-item:hover {
  background:#f3f4f6;
}

.layout {

display:flex;

gap:30px;

}


.main {

flex:3;

}


.side {

flex:1;

border-left:1px solid #ddd;

padding-left:20px;

}



.slide {

padding:12px;

margin-bottom:10px;

border:1px solid #ddd;

cursor:pointer;

}



.slide:hover {

background:#f3f4f6;

}



input {

width:80%;

padding:8px;

}



button {

margin-left:5px;

padding:8px 12px;

}



.answer {

margin-top:15px;

padding:10px;

background:#f5f5f5;

}

.active {
  background:#e5e7eb;
  border-color:#666;
}

.activeTime {
  background:#f3f4f6;
  font-weight:bold;
}

</style>