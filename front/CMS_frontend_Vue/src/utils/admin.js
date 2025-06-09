import api from './api.js'

const admin = {
    login(data){
        return api.post('/admin/login',data)
    },
    change_password(data){
        return api.post('/admin/changepassword',data)
    },
    logout(data){
        return api.post('/admin/logout',data)
    },
    register(data){
        return api.post('/admin/register',data)
    },
    deregister(data){
        return api.post('/admin/deregister',data)
    },
    get_teacher_info(data){
        return api.post('/admin/showteachers',data)
    },    
    get_class_info(data){
        return api.post('/admin/showclasses',data)
    },
    get_browsing_history(data){
        return api.post('/admin/showbrowses',data)
    },
    show_exceptions(data){
        return api.post('/admin/showexceptions',data)
    },
    delete_exception(data){
        return api.post('/admin/deleteexception',data)
    },
    show_class_students(data){
        return api.post('/admin/showclassstudents',data)
    },
    create_class(data){
        return api.post('/admin/createclass',data)
    },
    delete_class(data){
        return api.post('admin/deleteclass',data)
    },
    assign_class(data){
        return api.post('/admin/assignclass',data)
    },
    unassign_class(data){
        return api.post('/admin/unassignclass',data)
    },
    change_grade(data){
        return api.post('/admin/changegrade',data)
    },
    set_power(data){
        return api.post('/admin/setpower',data)
    },
    show_statistics(){
        return api.get('/admin/showstatistics')
    },
    show_all_students(data){
        return api.post('/admin/showallstudents',data)
    },
    create_student(data){
        return api.post('/admin/createstudent',data)
    },
    change_student_info(data){
        return api.post('/admin/changestudentinfo',data)
    },
    delete_student(data){
        return api.post('/admin/deletestudent',data)
    }


}

export default admin