const template=`
<h1>你的身分是: {{userID}}</h1>
<div v-if="pageMode=='edit'">
	id:{{record.id}} <br/>
	Job Name:<input type="text"	v-model="record.jobName" /><br />
	Job Content: <textarea v-model="record.jobContent"></textarea> <br/>
	Job Urgent <select v-model='record.jobUrgent'>
		<option value='high'>高</option>
		<option value='mid'>中</option>
		<option value='low'>低</option>
	</select>
	<br />
	<hr style='clear:both;'/>
	<input type='button' v-on:click='submitit()' value='Save'>
	<br/>
</div>
<div v-if="pageMode=='list'">
	<button @click="loadEditForm(-1)">Add Job</button>
	<table width="200" border="1">
	  <tr>
		<td>id</td>
		<td>Job Name</td>
		<td>Job Content</td>
		<td></td>
	  </tr>
		<tr v-for="rec in dat">
			<td>{{rec.id}}</td>
			<td>{{rec.jobName}}</td>
			<td>{{rec.jobContent}}</td>
			<td>
				<button @click="loadEditForm(rec.id)">Edit</button> 
				<button @click="delJob(rec.id)">del</button>
			</td>
		</tr>
	</table>

</div>
`;
	
const vueDef={
	data() {   //對應的資料在data裡面對應好
		return {
			dat: [],
			record:{
				jobID:-1,
				jobName:'',
				jobContent:'',
				jobUrgent:'low'
			},
			pageMode:'',
			userID:myID
		}
	},
	components:{},
	methods: {
		loadList() {
			let that=this;
			let url="getJobList";
			fetch(url)
			.then(function(resp){return resp.json();})
			.then(function(json) {
				//console.log(json)
				that.dat=json;
				that.pageMode='list';
			})			
		},
		submitit() {									
			let mydat = new FormData();
			//console.log(this.dat);
			//this is one way
			mydat.append( "dat", JSON.stringify(this.record) );				
			/*
			//this is another way
			for (key in dat) {
				mydat.append(key, dat[key])
			}
			*/
			//console.log(mydat)
			let that=this;
			let url="saveJob";
			fetch(url,{
				method: 'POST', 
				body: mydat									
			})
			.then(function(res){return res.text(); })
			.then(function(data){ 
				//console.log(data);
				that.loadList();
			})
		},
		loadEditForm(id) {
			this.pageMode='edit'; //變數設為edit，上面資料就會顯示其他藏起來
			let that=this;
			if (id== -1) {  //如果是-1代表他是要新增的
				this.record={  //把資料內容清成空的
					id:-1,
					jobName:'',
					jobContent:'',
					jobUrgent:'low'
				};
			}else {
				let mydat = new FormData();
				mydat.append( "id", id );
				let url="loadData";
				fetch(url,{
					method: 'POST', 
					body: mydat									
				})
				.then(function(res){return res.json(); })
				.then(function(data){
					//console.log(data);
					that.record=data;
					that.pageMode='edit';
				})
			}
		}, 
		delJob(id) {
			let mydat = new FormData();
			mydat.append( "id", id );
			let url="delJob";  //去request app.py裡面的delJob
			let that=this;
			fetch(url,{
				method: 'POST', 
				body: mydat									
			})
			.then(function(res){return res.text(); })
			.then(function(data){ 
				//console.log(data);
				that.loadList();  //callback裡面請他重新load清單
			})
		},
			
			
	},
	created() { //當她被建立的時候先執行的指令
		this.loadList();
	}
}

