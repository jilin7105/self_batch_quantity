         let post_data = {}

        const  vdo = $("#showVideo")
        $('.vidoe_tab').on('click', function (event) {
            console.log(event)
            let name = $(this).text()
            let url = $(this).data("url")
            console.log(url)
            vdo.attr("src",url)
            init(name)
            $('#myList a').removeClass("active")
            $(this).addClass("active")
        })

        function init(name) {
            post_data={}
            post_data.name = name
            post_data.fengmian = ""
            post_data.cutlist = []
            update()
        }
        function update() {
            let title = $("#title")
            title.html(post_data.name)
            let table_info = ""
            for (let i = 0; i < post_data.cutlist.length ; i++) {
                table_info += "<tr>" +
                    "<th scope=\"row\">"+i+"</th>" +
                    "<td>"+post_data.cutlist[i].start+"</td>" +
                    "<td>"+post_data.cutlist[i].end+"</td>"
            }
            $("table tbody").html(table_info)
            console.log(table_info)
        }

        $("#start").click(function () {
            let time = vdo[0].currentTime

            post_data.cutlist.push({"start":time ,"end":"NONE"})
            update()
        })
        $("#end").click(function () {
            let time = vdo[0].currentTime

            if(post_data.cutlist.length>0 && post_data.cutlist[post_data.cutlist.length-1].end=="NONE"){
                post_data.cutlist[post_data.cutlist.length-1].end= time
            }

            update()
        })

        $('#myModal').on('shown.bs.modal', function () {
            moduleInit()
        })

        function moduleInit() {
            let new_cutlist = []
            for (let i = 0; i < post_data.cutlist.length ; i++) {
                if(post_data.cutlist[i].start>0 && post_data.cutlist[i].end !== "NONE" ){
                    new_cutlist.push(post_data.cutlist[i])
                }
            }
            post_data.cutlist = new_cutlist
            $("#checkinfo").html(JSON.stringify(post_data))
            update()
        }


        $('#postModal').on('shown.bs.modal', function () {
            moduleInit()
        })


         $(".image_chack").on("click",function () {
            let name = $(this).data("url")
             post_data.fengmian = name
             moduleInit()
             $('#imageModal').modal('hide')
         })

         $("#save").click(function () {
               $.post("/cutvide",JSON.stringify(post_data),function(result){
                   console.log(result)
                    alert(JSON.parse(result))
               },"json");

               $('#postModal').modal('hide')
         })
