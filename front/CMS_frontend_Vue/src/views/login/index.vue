<template>
  <div style="margin: 0;padding:0">
    <div class="login-container" >
      
      <div>
          <img class="index-background" src="../../components/wallpaper.png" alt="">
      </div>
        <el-form ref="loginForm" :model="loginForm"  class="login-form" autocomplete="on" label-position="left">

      <div class="background-opacity-monk"></div>
        <div class="title-container">
          <h3 class="title">教室智能监控与分析系统</h3>
        </div>

        <el-form-item prop="username">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="用户名"
            name="username"
            type="text"
            tabindex="1"
            autocomplete="on"
          />
        </el-form-item>

        <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
          <el-form-item prop="password">
            <span class="svg-container">
              <svg-icon icon-class="password" />
            </span>
            <el-input
              :key="passwordType"
              ref="password"
              v-model="loginForm.password"
              :type="passwordType"
              placeholder="密码"
              name="password"
              tabindex="2"
              autocomplete="on"
              @keyup.native="checkCapslock"
              @blur="capsTooltip = false"
              @keyup.enter.native="handleLogin"
            />
            <span class="show-pwd" @click="showPwd">
              <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </el-form-item>
        </el-tooltip>
        <br>
        <el-button :loading="loading" 
                    type="primary" 
                    style="width:100%;margin-bottom:30px;border-radius: 10px;" 
                    @click="handleLogin">
                    登录
        </el-button>

      </el-form>
    </div>
  </div>
</template>

<script>
import admin from '@/utils/admin'

// import { validUsername } from '@/utils/validate'

export default {
  name: 'Login',
  data() {
    // const validateUsername = (rule, value, callback) => {
    //   if (!validUsername(value)) {
    //     this.$message({
    //       message:'用户名'
    //     })
    //     // callback(new Error('Please enter the correct user name'))
    //   } else {
    //     callback()
    //   }
    // }
    // const validatePassword = (rule, value, callback) => {
    //   if (value.length < 3) {
    //     callback(new Error('The password can not be less than 3 digits'))
    //   } else {
    //     callback()
    //   }
    // }
    return {
      loginForm: {
        username: 'admin',
        password: '123'
      },
      // loginRules: {
      //   username: [{ required: true, trigger: 'blur', validator: validateUsername }],
      //   password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      // },
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showDialog: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          // console.log('888888 this.redirect ---> ', this.redirect)
          this.otherQuery = this.getOtherQuery(query)
          // console.log('888888 this.otherQuery ---> ', this.otherQuery)
        }
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {
    if (this.loginForm.username === '') {
      this.$refs.username.focus()
    } else if (this.loginForm.password === '') {
      this.$refs.password.focus()
    }
  },
  methods: {
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      var data = {
        user_account: this.loginForm.username,
        password: this.loginForm.password
      }
      // console.log(data)
      var Response = {
        data:{
          'code':0,
          'msg':'登录成功'
        }
      }
      // admin.login(data).then(Response => {
        if (!Response.data['code']) {
          this.$message({
            message: Response.data['msg'],
            type: 'success'
          })
          
          localStorage.setItem('admin', data.user_account)
          // this.$router.push('/')
          this.$router.push({path:'/'})
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm)
            .then(() => {
              this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
              this.loading = false
            })
            .catch(() => {
              this.loading = false
            })
        } else {
          this.$message.error(Response.data['msg'])
          console.log('error submit!!')
          return false
        }
      // })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 75%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

.index-background{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 15px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  // background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 450px;
    max-width: 100%;
    padding: 130px 35px 100px 50px ;
    margin: 0 auto;
    margin-top: 160px;
    margin-bottom: 60px;
    overflow: hidden;
    backdrop-filter: blur(3px);
    border-left: 2px solid rgba(255, 255, 255, .3);
    border-top: 2px solid rgba(255, 255, 255, .3);
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, .4);
    background-color: rgba(255, 255, 255, 0.2);
  }


  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $light_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      opacity: .8;
      letter-spacing: 4px;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $light_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
