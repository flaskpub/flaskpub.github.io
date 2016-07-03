$(function(){
	var contaier = $('#message_container');
	var show_message = function(msg, msg_type, id) {
		if (typeof msg_type == 'undefined') msg_type = 'info';
		msg = $('<div/>').text(msg).html();
		msg = msg.replace("\n", "<br />");
		
		var template = $("<div><\/div>")
			.addClass('alert-message')
			.addClass('block-message')
			.addClass(msg_type);
		if (typeof id != 'undefined') {
			template.attr('id', id);
		}
		contaier.prepend(template.html(msg));
	};
	var update = function() {
		$.ajax({
			url: '/message/',
			type: 'get',
			dataType: 'json',
			success: function(r) {
				try {
					show_message(r.msg, 'info', r.id);
					update();
				} catch (e) {
					show_message('发生错误：' + e, 'alert');
				}
			},
			error: function(jqxhr, status, thrown) {
				if (status == 'abort' || status == 'timeout' || xhr.status == 0) return;
				show_message('与服务器通讯发生错误：' + status.toString(), 'error');
			}
		});
	};
	update();
	$('#message_form').submit(function(){
		$.ajax({
			url: '/message/',
			type: 'post',
			dataType: 'json',
			data: $(this).serialize(),
			success: function() {
				update();
				$("#chat_content").val("");
			},
			error: function(jqxhr, status) {
				if (status == 'abort') return;
				if (status != 'timeout') {
					show_message('向服务器发送消息时发生错误：' + status.toString(), 'error');
				}
				update();
			}
		});
		return false;
	});
});