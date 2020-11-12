<template>
    <div class="singles-question mt-2">
        <div class="container">
            <h1>{{ question.content }}</h1>
            <QuestionActions
                v-if="isQuestionAuthor"
                :slug="question.slug"
            />
            <p class="mb-0">Posted by:
                <span class="author-name">{{ question.author }}</span>
            </p>
            <p>{{ question.created_at }}</p>
            <hr>
            <div v-if="userHasAnswered">
                <p class="answer-added">You've written an answer</p>
            </div>
            <div v-else-if="showForm">
                <form class="card" @submit.prevent="onSubmit">
                    <div class="card-header px-3">
                        Answer The Question
                    </div>
                    <div class="card-block">
                        <textarea 
                            rows="5"
                            v-model="newAnswerBody"
                            class="form-control"
                            placeholder="Share your knowledge"
                        >
                        </textarea>
                    </div>
                    <div class="card-footer px-3">
                        <button type="submit" class="btn btn-sm btn-danger">Submit Answer</button>
                    </div>
                </form>
                <p v-if="error" class="error mt-2">{{ error }}</p>
            </div>
            <div v-else>
                <button class="btn btn-sm btn-danger"
                @click="showForm = true">
                Answer The Question</button>
            </div>
            <hr>
        </div>
        <div class="container">
            <AnswerComponent
                v-for="answer in answers"
                :answer="answer"
                :key="answer.id"
                :requestUser="requestUser"
                @delete-answer="deleteAnswer"
            />
            <div class="my-3">
                <p v-show="loadingAnswers">...loading...</p>
                <button
                    v-show="next"
                    @click="getQuestionAnswers"
                    class="btn btn-sm btn-outline-danger"
                    >Load More
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { apiService } from "../common/api.service.js"
import AnswerComponent from "@/components/Answer.vue"
import QuestionActions from "@/components/QuestionActions"
export default {
    name: "Question",
    props: {
        slug: {
            type: String,
            required: true
        }
    },
    components: {
        AnswerComponent,
        QuestionActions
    },
    data(){
        return{
            question: {},
            answers: [],
            newAnswerBody: null,
            error: null,
            userHasAnswered: false,
            showForm: false,
            next: null,
            loadingAnswers: false,
            requestUser: null,
        }
    },
    computed: {
        isQuestionAuthor() {
            return this.question.author === this.requestUser
        }
    },
    methods: {
        setPageTitle(title) {
            document.title = title
        },
        setRequestUser(){
            this.requestUser = window.localStorage.getItem("username")
        },
        getQuestionData() {
            let endpoint = `/api/questions/${this.slug}/`;
            apiService(endpoint).then(data=> {
                this.question = data;
                this.userHasAnswered = data.user_has_answered;
                this.setPageTitle(data.content)
            })
        },
        getQuestionAnswers() {
            let endpoint = `/api/questions/${this.slug}/answers/`;
            if (this.next){
				endpoint = this.next
            }
            this.loadingAnswers = true
            apiService(endpoint)
                .then(data => {
                    this.answers.push(...data.results)
                    this.loadingAnswers = false
                        if(data.next){
                            this.next = data.next
                        }
                        else{
                            this.next = null
                        }
                })
        },
        onSubmit() {
            if (this.newAnswerBody){
                let endpoint = `/api/questions/${this.slug}/answer/`;
                apiService(endpoint, "POST", { body: this.newAnswerBody })
                    .then(data => {
                        this.answers.unshift(data)
                    })
                this.newAnswerBody = null
                this.showForm = false
                this.userHasAnswered = true
                if(this.error){
                    this.error = null
                }
            }else{
                this.error = "You can't send an empty answer"
            }
        },
        async deleteAnswer(answer){
            let endpoint = `/api/answers/${answer.id}/`;
            try{
                await apiService(endpoint, "DELETE")
                this.$delete(this.answers, this.answers.indexOf(answer))
                this.userHasAnswered = false
            }
            catch(err){
                console.log(err)
            }
        }
    },    
    created(){
        this.getQuestionData()
        this.getQuestionAnswers()
        this.setRequestUser()
    }
}
</script>

<style>
    .author-name{
        font-weight: bold;
		color: crimson;
    }
    .answer-added{
        font-weight: bold;
        font-size: 16px;
    }
    .error{
        font-weight: bold;
        font-size: 16px;
    }
</style>