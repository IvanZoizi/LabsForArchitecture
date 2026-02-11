package labs2.models;

import labs2.views.View;

import java.util.List;

public interface Models<T> {

    List<T> get();
    boolean post(T data);
    boolean update(T data, T newData);
    boolean delete(T data);
}
