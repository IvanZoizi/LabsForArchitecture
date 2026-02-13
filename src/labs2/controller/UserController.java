package labs2.controller;

import labs2.models.Models;
import labs2.views.View;
import java.util.List;

public class UserController<T> implements Controller<T>{

    private final Models<T> model;
    private final View<T> view;

    public UserController(Models<T> model, View<T> view) {
        this.model = model;
        this.view = view;
    }

    @Override
    public void get() {
        List<T> data = model.get();
        view.updateData(data);
    }

    @Override
    public boolean post(T data) {
        if (model.post(data)) {
            this.get();
            return true;
        }
        return false;
    }

    @Override
    public boolean update(T data, T newData) {
        if (model.update(data, newData)) {
            this.get();
            return true;
        }
        return false;
    }

    @Override
    public boolean delete(T data) {
        if (model.delete(data)) {
            this.get();
            return true;
        }
        return false;
    }
}
