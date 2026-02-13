package labs2.controller;

import labs2.views.View;

public interface Controller<T> {
    void get();
    boolean post(T data);
    boolean update(T data, T newData);
    boolean delete(T data);
}
