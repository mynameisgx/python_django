#自定义分页组件
'''
#使用说明（视图函数中）
def pretty_list(request):
   #1.筛选数据
    queryset=PrettyNum.objects.filter(**data_dict).order_by('-level')
   #2.实例化分页对象
    page_object=Pagination(request,queryset)

    context={'queryset': page_object.page_queryset,#分完页的数据
             "search_data": search_data, #生成页码
             "page_string": page_object.html()}
    return render(request,'pretty_list.html',context)
    #在HTML中，
    {% for obj in queryset %}
    {{obj.xx}}
    {%endfor%}
    <ul class="pagination">
    {{ page_string }}
  </ul>
'''
from django.shortcuts import render
from django.utils.safestring import mark_safe


class Pagination(object):
    """
            :param request: 请求的对象
            :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
            :param page_size: 每页显示多少条数据
            :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
            :param plus: 显示当前页的 前或后几页（页码）
            """

    def __init__(self,request,queryset,page_size=10,page_param="page",plus=5):

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.quer_dict = query_dict
        self.page_param=page_param

        # query_dict.setlist('page', 11)
        # print(query_dict.urlencode())

        page = request.GET.get(page_param, 1)#整形
         # if page.isdecimal():#如果是十进制的数
         #     page=int(page)#这样得到的page就是整形
         # else:
         #     page=1
        self.page=page
        self.page_size=page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset=queryset[self.start:self.end]
        self.plus=plus
        self.query_dict=query_dict
        total_count = queryset.count()#获取数据总条数
         # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count=total_page_count
        self.page_param=page_param

        #获取页码
    def html(self):
             plus=5
             if self.total_page_count <= 2 * self.plus + 1:
                 # 数据库中的数据较少，小于11页
                 start_page = 1
                 end_page = self.total_page_count
             else:
                 # 数据库中的数据较多，大于11页
                 # 当前页<5时
                 if self.page <= self.plus:
                     start_page = 1
                     end_page = 2 * self.plus + 1 + 1
                 else:
                     # 当前页>5
                     if (self.page + self.plus) > self.total_page_count:
                         start_page = self.total_page_count - 2 * self.plus
                         end_page = self.total_page_count
                     else:
                         start_page = self.page - self.plus
                         end_page = self.page + self.plus + 1
                 # 页码
             page_str_list = []

             self.query_dict.setlist(self.page_param, [1])

             page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

             # 上一页
             if self.page > 1:
                 self.query_dict.setlist(self.page_param, [self.page- 1])
                 prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
             else:
                 self.query_dict.setlist(self.page_param, [1])
                 prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
             page_str_list.append(prev)
            #页面
             for i in range(start_page, end_page):  # 注意要加1，因为range前取后不取
                 self.query_dict.setlist(self.page_param, [i])
                 if i == self.page:
                     ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)  # 显示当前页
                 else:
                     ele = '<li class="disable"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                 page_str_list.append(ele)

             # 下一页
             if self.page < self.total_page_count:
                 self.query_dict.setlist(self.page_param, [self.page+1])
                 prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
             else:
                 self.query_dict.setlist(self.page_param, [self.total_page_count])
                 prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
             page_str_list.append(prev)

             # 页尾
             page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count))

             search_string = '''
                 <li>
                       <form method="get" style="display: inline-block;float: left;position: relative">
                     <div class="input-group" style="width: 200px">
                         <input type="text" name="page" class="form-control" placeholder="页码" >
                         <span class="input-group-btn">
                             <button class="btn btn-default" type="submit">跳转</button>
                         </span>
                     </div>
                 </form>
                   </li>
                 '''
             page_str_list.append(search_string)

             page_string = mark_safe("".join(page_str_list))  # 确保是安全数据
             return page_string
