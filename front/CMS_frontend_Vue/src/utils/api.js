import axios from 'axios'

const api = axios.create({
    baseURL:"http://10.203.136.86:4000",
    timeout:"5000"
})

export default api