import {
  FETCH_START,
  FETCH_END, RESET_FETCH
} from './mutations.type'

import {
  FETCH_CLASSIFY
} from './actions.type'
import {
  ClassifyService
} from '@/common/api.service'

const state = {
  result: [],
  isLoading: false,
  errors: null
}

const getters = {
  result(state) {
    return state.result
  },
  isLoading(state) {
    return state.isLoading
  },
  errors(state) {
    return state.errors
  },

}

const actions = {
  [FETCH_CLASSIFY]({commit}, {slug, payload}) {
    commit(FETCH_START)
    return ClassifyService.post(slug, payload)
      .then(({data}) => {
        if (data.errors !== null) {
          commit(FETCH_END, {result: null, errors: data.errors})
        }
        else {
          commit(FETCH_END, {result: data.data.predicted_result, errors: null})
        }
      })
      .catch((error) => {
        throw new Error(error)
      })
  },
  [RESET_FETCH]({commit}) {
    commit(RESET_FETCH)
  }
}

/* eslint no-param-reassign: ["error", { "props": false }] */
const mutations = {
  [FETCH_START](state) {
    state.isLoading = true
  },
  [FETCH_END](state, {result, errors}) {
    state.result = result
    state.isLoading = false
    state.errors = errors
  },
  [RESET_FETCH](state) {
    state.result = []
    state.isLoading = false
    state.errors = null
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
