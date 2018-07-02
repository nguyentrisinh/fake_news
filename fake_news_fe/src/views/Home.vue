<template>
  <div class="container">
    <div class="row align-items-center justify-content-center">
      <div class="col-6">
        <img src="../assets/images/real-or-fake.jpg" class="img-fluid">
      </div>
    </div>
    <h1 class="text-center mt-3 mb-3">Kiểm định tin tức</h1>
    <div class="row">
      <div class="col-6">
        <form action="">
          <div class="row">
            <div class="form-group col-4">
              <label for="type">Chọn phương pháp</label>
              <select v-on:change="resetFetch" v-model="selected" id="type" class="form-control">
                <option v-for="option in options" v-bind:value="option.value">
                  {{ option.text }}
                </option>
              </select>
            </div>

            <div class="form-group col-4">
              <label for="type">Chọn cách kiểm định</label>
              <select v-on:change="resetFetch" v-model="typeSelected" class="form-control">
                <option v-for="option in optionsType" v-bind:value="option.value">
                  {{ option.text }}
                </option>
              </select>
            </div>
            <div class="text-center col-4">
              <div class="form-group">
                <label for="">&nbsp;</label>
                <button v-on:click="fetchClassify" type="submit" class="form-control btn btn-primary mb-3 bg-purple">
                  Kiểm định &nbsp;<i
                  class="zmdi zmdi-chevron-right"></i></button>
              </div>

            </div>
          </div>
          <div class="form-group">
            <label for="content">Nội dung cần kiểm định</label>
            <!--<div> {{content}}</div>-->
            <textarea v-on:input="resetFetch" v-model="content" placeholder="Nhập nội dung cần kiểm định"
                      class="form-control" id="content" rows="14"/>
          </div>
        </form>
      </div>
      <div class="col-6">
        <!--<div v-if="isLoading" class="article-preview">-->
        <!--Loading Data...-->
        <!--</div>-->
        <!--<div v-else>-->
        <div v-if="!!errors">
          <div class="text-danger">
            Lỗi
          </div>
        </div>
        <div v-else>
          <label for=""> Kết quả kiểm định</label>
          <ul class="list-group position-relative">
            <div v-if="typeSelected==='sentence'">
              <li class="media align-items-center list-group-item"
                  v-bind:class="result?{'list-group-item-danger':result[index]===2,'list-group-item-success':result[index]===1}:''"
                  v-if="!!value.trim()" v-for="(value,index) in contentArray">
                <div class="media-body">
                  {{value}}
                </div>
              </li>
            </div>
            <div v-if="typeSelected==='full'">
              <li class="media align-items-center list-group-item"
              v-bind:class="result?{'list-group-item-danger':result[0]===2,'list-group-item-success':result[0]===1}:''"
                  v-if="!!content.trim()"
              >
                <div class="media-body">
                  {{content}}
                </div>
              </li>
            </div>

            <li v-if="!hasContentArray" class="list-group-item list-group-item-danger">
              Nhập nội dung tin và ấn vào nút "Kiểm định" để thực hiện chương trình
            </li>
            <div v-if="isLoading"
                 class="position-absolute position-center overlap d-flex align-items-center justify-content-center">
              <div class="lds-ellipsis">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
              </div>
            </div>
          </ul>

        </div>

        <!--</div>-->

      </div>
    </div>
    <div class="row justify-content-center align-items-center mb-5">

    </div>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  import {FETCH_CLASSIFY} from '@/store/actions.type'
  import {RESET_FETCH} from '@/store/mutations.type'

  export default {
    name: 'home',
    computed: {
      ...mapGetters([
        'result',
        'isLoading',
        'errors',
      ]),
      contentArray() {
        return this.$data.content.split('.')
      },
      hasContentArray() {
        return !!this.$data.content.trim()
      }
    },
    data() {
      return {
        content: '',
        options: [
          {text: 'Decision Tree', value: 'decision_tree'},
          {text: 'Naive Bayes', value: 'naive_bayes'},
          {text: 'SVM', value: 'svm'}
        ],
        typeSelected: 'full',
        optionsType: [
          {text: 'Theo câu', value: 'sentence'},
          {text: 'Toàn bộ tin', value: 'full'},
        ],
        selected: 'svm',
      }
    },
    methods: {
      fetchClassify() {
        console.log(this.$data.typeSelected)
        if (this.$data.typeSelected==='sentence'){
          this.$store.dispatch(FETCH_CLASSIFY, {slug: this.$data.selected, payload: this.contentArray})
        }
        else{
          this.$store.dispatch(FETCH_CLASSIFY, {slug: this.$data.selected, payload: [this.$data.content]})
        }
      },
      resetFetch() {
        this.$store.dispatch(RESET_FETCH)
      }
    }
  }
</script>

<style scoped>

</style>
