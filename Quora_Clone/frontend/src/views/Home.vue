<template>
<div class="home">
	<div class="container">
		<div v-for="question in questions" :key="question.pk">
			<p class="mb-0">Posted by:
				<span class="question-author">{{ question.author }}</span>
			</p>
			<h2>
				<router-link
					:to="{ name: 'question', params: { slug: question.slug } }"
					class="question-link"
					>{{ question.content }}
				</router-link>
			</h2>
			<p>Answers: {{question.answers_count }}</p>
		</div>
	</div>
</div>
</template>

<script>
import { apiService } from "../common/api.service.js"

export default {
	name: "Home",
	data(){
		return {
			questions: []
		}
	},
	methods:{
		getQuestions(){
			let endpoint = "api/questions/"
			apiService(endpoint)
				.then(data => {
					this.questions.push(...data.results)
				})
		}
	},
	created(){
		this.getQuestions()
		document.title = "QuoraClone"
	}
};
</script>

<style lang="css" scoped>
	.question-author{
		font-weight: bold;
		color: crimson;
	}

	.question-link{
		font-weight: bold;
		color: black;
	}
	.question-link:hover{
		color: #343A40;
		text-decoration: none;
	}
</style>
	