/**
 * Created by 123 on 2017/9/26.
 */
odoo.define('petstore.employee_view', function (require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
	var View = require('web.View');
    var data = require('web.data');
    var formats = require('web.formats');
    var common = require('web.form_common');
    var framework = require('web.framework');
    var datepicker = require('web.datepicker');
    var QWeb = core.qweb;
    var _t = core._t;
    var myself;

    Date.prototype.Format = function (fmt) { //author: meizz
        var o = {
            "M+": this.getMonth() + 1,                 //月份
            "d+": this.getDate(),                    //日
            "h+": this.getHours(),                   //小时
            "m+": this.getMinutes(),                 //分
            "s+": this.getSeconds(),                 //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds()             //毫秒
        };
        if (/(y+)/.test(fmt))
            fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt))
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }

    var Employee_View = View.extend({
        template: 'employee_view_template_wrap',
		view_type: "employee_view",
		events:{
			'click .dhx_cal_navline':'func',
			'onload window': 'func1'
		},
		func1:function () {
			console.log('sssssss')
		},
		func:function () {
			console.log($("#scheduler_here"))
		},
        init: function (parent, options) {
            var self = this;
            this._super.apply(this, arguments);
            this.has_been_loaded = $.Deferred();
            this.chart_id = _.uniqueId();
        },

        start: function () {
			console.log(this.$el);
			return this.load_view();
        },
        load_view: function (context) {
            var self = this;
            var view_loaded_def;
            if (this.embedded_view) {
                view_loaded_def = $.Deferred();
                $.async_when().done(function () {
                    view_loaded_def.resolve(self.embedded_view);
                });
            } else {
                if (!this.view_type)
                    console.warn("view_type is not defined", this);
                view_loaded_def = fields_view_get({
                    "model": this.dataset._model,
                    "view_id": this.view_id,
                    "view_type": this.view_type,
                    "toolbar": !!this.options.$sidebar,
                    "context": this.dataset.get_context(),
                });
            }
            return this.alive(view_loaded_def).then(function (r) {
                self.fields_view = r;
                return $.when(self.view_loading(r)).then(function () {
                    self.trigger('view_loaded', r);
                });
            });
        },
        view_loading: function (r) {
            return this.load_gantt(r);
        },
        load_gantt: function (fields_view_get, fields_get) {
            var self = this;
            this.fields_view = fields_view_get;
            this.$el.addClass(this.fields_view.arch.attrs['class']);
            return self.alive(new Model(this.dataset.model)
                .call('fields_get')).then(function (fields) {
                self.fields = fields;
                self.has_been_loaded.resolve();
            });
        },
        do_search: function (domains, contexts, group_bys) {
            var self = this;
            if (domains) {
                _.each(domains, function (domain, i) {
                    if (domain && domain[0] == "parent_ids") {
                        domains.splice(i, 1);
                    }
                });
            }
            self.last_domains = domains;
            self.last_contexts = contexts;
            self.last_group_bys = group_bys;
            // select the group by
            var n_group_bys = [];
            if (this.fields_view.arch.attrs.default_group_by) {
                n_group_bys = this.fields_view.arch.attrs.default_group_by.split(',');
            }
            if (group_bys.length) {
                n_group_bys = group_bys;
            }
            // gather the fields to get
            var fields = _.compact(_.map(["name", "address_id", "gender", "passport_id","work_email","work_phone","identification_id","image"], function (key) {
                return self.fields_view.arch.attrs[key] || '';
            }));
            fields = _.uniq(fields.concat(n_group_bys));

            return $.when(this.has_been_loaded).then(function () {
                return self.dataset.read_slice(fields, {
                    domain: domains,
                    context: contexts
                }).then(function (data) {
                    return self.on_data_loaded(data, n_group_bys);
                });
            });
        },
        reload: function () {
            if (this.last_domains !== undefined)
                return this.do_search(this.last_domains, this.last_contexts, this.last_group_bys);
        },
        on_data_loaded: function (tasks, group_bys) {
            var self = this;
            var ids = _.pluck(tasks, "id");
            return this.dataset.name_get(ids).then(function (names) {
                var ntasks = _.map(tasks, function (task) {
                    return _.extend({
                        __name: _.detect(names, function (name) {
                            return name[0] == task.id;
                        })[1]
                    }, task);
                });
                return self.on_data_loaded_2(ntasks, group_bys);
            });
        },
        on_data_loaded_2: function (tasks, group_bys) {
            var self = this;
            console.log(tasks);
            $(".o_content").append(self.$el[0]);
            self.$el.html('');
            self.$el.append(QWeb.render('employee_view_template',{result:tasks}));

        },
    });

	var fields_view_get = function (args) {
        function postprocess(fvg) {
            var doc = $.parseXML(fvg.arch).documentElement;
            fvg.arch = xml_to_json(doc, (doc.nodeName.toLowerCase() !== 'kanban'));
            if ('id' in fvg.fields) {
                // Special case for id's
                var id_field = fvg.fields['id'];
                id_field.original_type = id_field.type;
                id_field.type = 'id';
            }
            _.each(fvg.fields, function (field) {
                _.each(field.views || {}, function (view) {
                    postprocess(view);
                });
            });
            return fvg;
        }

        args = _.defaults(args, {
            toolbar: false,
        });
        var model = args.model;
        if (typeof model === 'string') {
            model = new Model(args.model, args.context);
        }
        return args.model.call('fields_view_get', {
            view_id: args.view_id,
            view_type: args.view_type,
            context: args.context,
            toolbar: args.toolbar
        }).then(function (fvg) {
            return postprocess(fvg);
        });
    };

    var xml_to_json = function (node, strip_whitespace) {
        switch (node.nodeType) {
            case 9:
                return xml_to_json(node.documentElement, strip_whitespace);
            case 3:
            case 4:
                return (strip_whitespace && node.data.trim() === '') ? undefined : node.data;
            case 1:
                var attrs = $(node).getAttributes();
                _.each(['domain', 'filter_domain', 'context', 'default_get'], function (key) {
                    if (attrs[key]) {
                        try {
                            attrs[key] = JSON.parse(attrs[key]);
                        } catch (e) {
                        }
                    }
                });
                return {
                    tag: node.tagName.toLowerCase(),
                    attrs: attrs,
                    children: _.compact(_.map(node.childNodes, function (node) {
                        return xml_to_json(node, strip_whitespace);
                    })),
                };
        }
    };

    core.view_registry.add('employee_view', Employee_View);
    return Employee_View;
})
