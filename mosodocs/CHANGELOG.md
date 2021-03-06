## 说明

1. 此文件主要用于记录关于此仓库的每一次修改的原因位置等情况


## 记录详情

1. 多个视频在一个页面时只有一个视频cc字幕可以移动
    - commit message: fix: closed caption can't move when mutiple videos in one page

2. 访问/sysadmin/courses页面时，后端报错
    - commit message: fix: Yields a 500 CODE error when opening /sysadmin/courses

3. 考试状态提醒无法显示翻译后文字
    - commit message: 修复BUG：考试状态提醒无法显示翻译后文字

4. 禁止用户自动注册与激活账户
    - commit message: 禁止发送激活账户的邮件

5. 更改MathJax.js的CDN地址
    - commit message: 更换MathJax.js的CDN地址

6. 手风琴目录添加小对勾标识
    - commit message: 手风琴目录显示完成与否标识

7. 自定义主题样式钩子
    - commit message: 自定义主题无法适配underscore文件，这里是在源码做的修改

8. 更新翻译文件，重新编译部分静态文件
    - commit message: 更新翻译文件及编译

9. 二次开发后台管理系统mosoadmin，独立的代码库
    - commit message: 添加mosoadmin钩子

10. 更改了一些配置参数
    - commit message: 更改了一些配置参数

11. 字幕默认打开与关闭问题
    - commit message: fix：右侧字幕默认显示及设置cookie问题 

12. 一个页面上第二个视频没有字幕也会出现cc字幕框
    - commit message: fix：一个页面上第二个视频没有字幕也会出现cc字幕框

13. 分布式部署预准备：解决django存储离线文件一致性问题
    - commit message: django文件存储引擎使用aliyun oss
    - 环境要求：
    ```sh
    pip install oss2==2.6.1 -i https://pypi.doubanio.com/simple/
    pip install git+https://github.com/jerrybox/django-oss-storage.git@mosoH2
    ```

14. 使用自定义的ora2包实现开放式问答题上传文件到阿里云
    ```sh
    which
    pip uninstall ora2
    pip install --no-deps git+https://github.com/jerrybox/edx-ora2.git@mosoH2 -i https://pypi.doubanio.com/simple/
    ```

15. 为了实现仅仅让ExamGroup组的学员能够看到显示考试的内容做了如下修改
```python
# vim /edx/app/edxapp/edx-platform/lms/djangoapps/courseware/module_render.py +196
# dir(section) 有几个重要属性 is_timed_exam，is_time_limited，group_access

course_groups = user.course_groups.filter(course_id=course.id)
timed_exam_visible = "ExamGroup" in (cg.name for cg in course_groups) or has_access(user, "staff", course)  or has_access(user, "instructor", course)

if section.is_timed_exam and not timed_exam_visible:
    continue
```
